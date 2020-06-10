from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from core.models import Transaction, User, Book
from core.permissions import IsEmployee
from core.filters import TransactionFilter
from .serializers import TransactionSerializer


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.filter(is_active=True)
    serializer_class = TransactionSerializer
    permission_classes = [IsEmployee]
    authentication_classes = (TokenAuthentication,)

    filterset_class = TransactionFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset()).filter()
        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        res = {'message': 'You can not delete Transactions.'}
        return Response(res, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk=None):
        data = request.data
        queryset = self.filter_queryset(self.get_queryset()).filter(id=pk)
        transaction = get_object_or_404(queryset)
        if 'complete' in data:
            transaction.is_active = False
            res = {'message': 'Transaction has been Completed.'}
            sts = status.HTTP_202_ACCEPTED
        if 'renew' in data:
            if transaction.renewals < 5:
                transaction.renewals = transaction.renewals + 1
                res = {'message': 'Transaction Renewed for 15 days', 'due_date': transaction.due_date()}
                sts = status.HTTP_202_ACCEPTED
            else:
                res = {'message': 'Can not renew transaction. Maximum number of renewals reached'}
                sts = status.HTTP_406_NOT_ACCEPTABLE
        transaction.save()
        return Response(res, status=sts)

    def create(self, request):
        data = request.data
        user = get_object_or_404(User.objects.filter(id=data['user']))
        book = get_object_or_404(Book.objects.filter(id=data['book']))
        query = self.filter_queryset(self.get_queryset()).filter(book__id=data['book'])
        if query:
            transaction = get_object_or_404(query)
            res = {'message': 'The requested book is already taken.', 'due_date': transaction.due_date()}
            sts = status.HTTP_400_BAD_REQUEST
        else:
            transaction = Transaction.objects.create(
                user=user,
                book=book,
                is_active=True,
                renewals=0
            )
            transaction.save()
            serializer = TransactionSerializer(transaction, many=False)
            res = {'message': 'New Transaction Added', 'result': serializer.data}
            sts = status.HTTP_201_CREATED
        return Response(res, sts)

