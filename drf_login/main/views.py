from rest_framework import generics, viewsets
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView, )
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import userProfile, Good, Check, Transaction
from .license import IsOwnerProfileOrReadOnly
from .serializer import userProfileSerializer, GoodSerializer, CheckSerializer
from crypto.Hash import SHA1
from .setting import private_key


class UserProfileListCreateView(ListCreateAPIView):
    queryset = userProfile.objects.all()
    serializer_class = userProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class userProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset = userProfile.objects.all()
    serializer_class = userProfileSerializer
    permission_classes = [IsOwnerProfileOrReadOnly, IsAuthenticated]


class GoodAPIView(generics.ListAPIView):
    queryset = Good.objects.all()
    serializer_class = GoodSerializer


class BuyAPIView(APIView):
    serializer_class = CheckSerializer

    async def post(self, request, *args, **kwargs):

        if request.method == "POST":
            good_id = request.POST.get('good_id')

            check_id = request.POST.get('check_id')

            good_to_buy = Good.objects.all()
            check_to_buy = Check.objects.all()
            check_post = check_to_buy[int(check_id) - 1]
            good_post = good_to_buy[int(good_id) - 1]
            price = good_post.price
            balance = check_post.balance
            if balance >= price:
                balance_after = balance - price

                check_ex = Check.objects.get(id=int(check_id))

                check_ex.balance = balance_after
                check_ex.save()

                trans = Transaction(indif=Check.objects.get(id=int(check_id)), summ=price)
                trans.save()
            else:
                pass


class BalanceAPIView(APIView):
    renderer_classes = [JSONRenderer]
    serializer_class = CheckSerializer

    async def post(self, request):
        indif = []
        balancee = []
        balance = Check.objects.all()
        for obj in balance:
            indif.append(str(obj.user))

            balancee.append(obj.balance)
        trance = Transaction.objects.all()
        history = []
        for obj in trance:
            history.append(obj.history)

        content = [{'history': history}, {'indif': indif}, {'blalnce': balancee}]

        return Response(content)


class PaymentAPIView(APIView):

    async def post(self, request):
        if request.method == "POST":
            amount = request.POST.get('amount')
            transaction = request.POST.get('transaction_id')
            user = request.POST.get('user_id')
            check = request.POST.get('bill_id')
            signature = request.POST.get('signature')
            signature_true = SHA1.new() \
                .update(f'{private_key}:{transaction}:{user}:{check}:{amount}'.encode()) \
                .hexdigest()
            # print(signature_true)
            if signature == signature_true:
                odj = Check.objcets.get(id=check)
                odj.balance = odj.balance + int(amount)
                odj.save
