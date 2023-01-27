from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.hashers import check_password, make_password

from .serializers import MemberSerializer
from .models import Member

class MemberRegisterView(
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    serializer_class = MemberSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, args, kwargs)

class MemberChangePassWordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        current = request.data.get('current')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        
        if password1 != password2:
            return Response({
                'detail1': 'Wrong new passwords',
            }, status = status.HTTP_400_BAD_REQUST)
        
        member = request.user 

        if not check_password(current, member.password):
            return Response({'detail1': 'Wrong new passwords',
            }, status = status.HTTP_400_BAD_REQUST)

        member.user.password=make_password(password1)
        member.user.save()

        return Response(status=status.HTTP_200_OK)