from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.authtoken.views import ObtainAuthToken

from .models import MyUser,Patient,HealthWorker,Request
from .serializers import UserSerializer, PatientSerializer, HealthWorkerSerializer, RequestSerializer

class CustomAuth(ObtainAuthToken):

  def post(self, request, *args, **kwargs):
    user = MyUser.objects.get(phone=request.data['phone'])
    token, created = Token.objects.get_or_create(user=user)
    serialize = UserSerializer(user)
    return Response({
        'token': token.key,
        'user': serialize.data
    })

class PatientViewSet(viewsets.ModelViewSet):
  queryset = Patient.objects.all()
  serializer_class = PatientSerializer
  permission_classes = (AllowAny,)

  def create(self, request, *args, **kwargs):
    if 'phone' and 'name' and 'bedno' and 'age' in request.data:
      user = MyUser.objects.create(phone=request.data['phone'],name=request.data['name'],is_doc=False)
      user.set_password(request.data['password'])
      user.save()
      Token.objects.create(user=user)
      patient = Patient.objects.create(pat=user,bed_no=request.data['bedno'],age=request.data['age'])
      patient.save()
      serializer = PatientSerializer(patient)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
      response = {'message': 'provide all details'}
      return Response(response, status=status.HTTP_400_BAD_REQUEST)

  @action(detail=True,methods=['GET'])
  def current(self, request, pk=None):
    usr = Patient.objects.get(id=pk)
    reqs = Request.objects.filter(patient=usr, is_done=False)
    serializer = RequestSerializer(reqs, many=True)
    return Response({'requests': serializer.data}, status=status.HTTP_200_OK)

  @action(detail=True,methods=['GET'])
  def history(self, request, pk=None):
    usr = Patient.objects.get(id=pk)
    reqs = Request.objects.filter(patient=usr, is_done=True)
    serializer = RequestSerializer(reqs, many=True)
    return Response({'requests': serializer.data}, status=status.HTTP_200_OK)

class HealthWorkerViewSet(viewsets.ModelViewSet):
  queryset = HealthWorker.objects.all()
  serializer_class = HealthWorkerSerializer
  permission_classes = (AllowAny,)

  def create(self, request, *args, **kwargs):
    if 'phone' and 'name' and 'is_doc':
      user = MyUser.objects.create(phone=request.data['phone'],name=request.data['name'],is_doc=True)
      user.set_password(request.data['password'])
      user.save()
      Token.objects.create(user=user)
      hw = HealthWorker.objects.create(doc=user, is_doc=request.data['is_doc'])
      hw.save()
      serializer = HealthWorkerSerializer(hw)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
      response = {'message': 'provide proper details'}
      return Response(response, status=status.HTTP_400_BAD_REQUEST)

  @action(detail=True,methods=['GET'])
  def current(self, request, pk=None):
    usr = HealthWorker.objects.get(id=pk)
    reqs = Request.objects.filter(hworker=usr,is_done=False)
    serializer = RequestSerializer(reqs, many=True)
    return Response({'requests': serializer.data}, status=status.HTTP_200_OK)

  @action(detail=True,methods=['GET'])
  def history(self, request, pk=None):
    usr = HealthWorker.objects.get(id=pk)
    reqs = Request.objects.filter(hworker=usr, is_done=True)
    serializer = RequestSerializer(reqs, many=True)
    return Response({'requests': serializer.data}, status=status.HTTP_200_OK)

class RequestViewSet(viewsets.ModelViewSet):
  queryset = Request.objects.all()
  serializer_class = RequestSerializer
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)

  def create(self, request, *args, **kwargs):
    # if request.data['is_critical']:
    #   req = Request.objects.create(patient=request.user,is_critical=request.data['is_critical'])
    #   notdone = Request.objects.filter(is_done = False)
    #   beds = []
    #   for pati in notdone:
    #     beds.append(Patient.objects.get(id=pati.patient).bed_no)
    #   beds.sort()
    #   for i in range(len(beds)):
    #     if beds[i] == request.user.bed_no:
    #       bed = beds[i-1]
    #       break
    pat = Patient.objects.get(pat=request.user)
    if request.data['is_critical']=='0':
      req = Request.objects.create(patient=pat, is_critical=request.data['is_critical'])
      docs = HealthWorker.objects.filter(is_free=True,is_doc=False).order_by("req_cnt")
      if len(docs)==0:
        reqs = Request.objects.filter(is_done=False,is_critical=False)
        hw = reqs[0].hworker
        hw.is_free = False
        hw.req_cnt+=1
        hw.save()
        req.hworker = hw
        req.save()
        serializer = RequestSerializer(req)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
      hw = docs[0]
      hw.is_free = False
      hw.req_cnt+=1
      hw.save()
      req.hworker = hw
      req.save()
      serializer = RequestSerializer(req)
      return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
      req = Request.objects.create(patient=pat, is_critical=request.data['is_critical'])
      docs = HealthWorker.objects.filter(is_free=True,is_doc=True).order_by("req_cnt")
      if len(docs)==0:
        reqs = Request.objects.filter(is_done=False,is_critical=True)
        hw = reqs[0].hworker
        hw.is_free = False
        hw.req_cnt+=1
        hw.save()
        req.hworker = hw
        req.save()
        serializer = RequestSerializer(req)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
      hw = docs[0]
      hw.is_free = False
      hw.req_cnt+=1
      hw.save()
      req.hworker = hw
      req.save()
      serializer = RequestSerializer(req)
      return Response(serializer.data,status=status.HTTP_201_CREATED)

  @action(detail=True, methods=['POST'])
  def on_done(self, request, pk=None):
    req = Request.objects.get(id=pk)
    req.is_done = True
    req.save()
    hw = HealthWorker.objects.get(doc=request.user)
    reqs = Request.objects.filter(hworker=hw,is_done=False)
    if len(reqs)==0:
      hw.is_free = True
      hw.save()
    msg = {'message':'Update successful'}
    return Response(msg, status=status.HTTP_200_OK)