from django.shortcuts import render

from django.db.models import Prefetch

from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from .models import Company, CompanyBank, Medicine, MedicalDetails
from .serializers import CompanySerializer, CompanyBankSerializer, MedicineSerializer, \
    MedicalDetailsSerializer, MedicalDetailsSerializerSimple, JoinMedicalDetailsSerializer, \
    ReverseCompanySerializer


class CompanyViewSet(viewsets.ViewSet):
# class CompanyViewSet(viewsets.ModelViewSet):
    # queryset = Company.objects.all()
    # serializer_class = CompanySerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def list(self, request):
        company = Company.objects.all()
        serializer = CompanySerializer(company, many=True, context={"request": request})
        dicr_response = {"error": False, "message": "All Company List Data", "data": serializer.data }
        return Response(dicr_response)

    def create(self,request):
        try:
            serializer = CompanySerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response= {"error": False, "message": "Company data save successfully"}
        except:
            dict_response = {"error": True, "message": "Error saving company data"}
        return Response(dict_response)

    def update(self,request, pk= None):
        try:
            queryset = Company.objects.all()
            company = get_object_or_404(queryset, pk=pk)
            serializer = CompanySerializer(company, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Company data update successfully"}
        except:
            dict_response = {"error": True, "message": "Error updating company data"}
        return Response(dict_response)

class CompanyBankViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        companybank = CompanyBank.objects.all()
        serializer = CompanyBankSerializer(companybank, many=True, context={"request": request})
        dicr_response = {"error": False, "message": "All Companybank List Data", "data": serializer.data }
        return Response(dicr_response)

    def create(self,request):
        try:
            serializer = CompanyBankSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response= {"error": False, "message": "Companybank data save successfully"}
        except:
            dict_response = {"error": True, "message": "Error saving companybank data"}
        return Response(dict_response)

    def retrieve(self,request, pk=None):
        queryset = CompanyBank.objects.all()
        companybank = get_object_or_404(queryset, pk=pk)
        serializer = CompanyBankSerializer(companybank, context={"request": request})
        return Response({"error": False, "message": "Companybank single data fetch", "data": serializer.data })

    def update(self, request, pk=None):
        queryset = CompanyBank.objects.all()
        companybank = get_object_or_404(queryset,pk=pk)
        serializer = CompanyBankSerializer(companybank, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"error":False, "message":"compnaybank data is updated successfully"})

class CompanyNameViewSet(generics.ListAPIView):
    serializer_class = CompanySerializer
    def get_queryset(self):
        name = self.kwargs["name"]
        return Company.objects.filter(name=name)


class MedicineViewSet(viewsets.ViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        medicines = Medicine.objects.all()
        serializer = MedicineSerializer(medicines, many=True, context={"request": request})
        medicine_data = serializer.data

        combine_medicine_list = []
        # Adding extra key medicine_details in medicine
        for medicine in medicine_data:
            # Accessing all medicine details of current medicine id
            id = medicine["id"]
            print(id)
            # medicine_details = MedicalDetails.objects.filter(medicine_id=medicine["id"])
            medicine_details = MedicalDetails.objects.filter(medicine_id=id)
            print(medicine_details)
            medicine_detail_serializers = MedicalDetailsSerializerSimple(medicine_details, many=True)
            print(medicine_detail_serializers.data)
            medicine['medicine_details'] = medicine_detail_serializers.data

            combine_medicine_list.append(medicine)



        dicr_response = {"error": False, "message": "All medicine List Data", "data": combine_medicine_list }
        return Response(dicr_response)

    def create(self,request):
        try:
            serializer = MedicineSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print("saving data")
            # Access th serializer id which we just save in our DB
            medicine_id = serializer.data['id']
            # print(medicine_id)
            medicine_detail_list = []
            for medicine_detail in request.data['medicine_detail']:
                # print(medicine_detail)
                # adding medicine id which will fork for MedicalDetail Serializer
                medicine_detail['medicine_id'] = medicine_id
                medicine_detail_list.append(medicine_detail)
                print(medicine_detail)

            serializer2 = MedicalDetailsSerializer(data=medicine_detail_list, many=True, context={"request": request})
            serializer2.is_valid()
            serializer2.save()

            dict_response= {"error": False, "message": "medicine data save successfully"}
        except:
            dict_response = {"error": True, "message": "Error saving medicine data"}

            # Json sample
            # {
            #     "company_id": 2,
            #     "name": "ffffff",
            #     "medical_typ": "nose",
            #     "buy_price": "887",
            #     "sell_price": "234",
            #     "c_gst": "23",
            #     "s_gst": "76",
            #     "batch_no": "8876",
            #     "shelf_no": "7876",
            #     "expire_date": "2021-03-08",
            #     "mfg_date": "2021-03-08",
            #     "description": "Slim, classic t-shirt .ultra soft fabric, with a worn in feel. Retains color, shape and softness. Machine wash cold. Use only non-chlorine bleach when needed. Tumble dry low. Do not use Iron on design",
            #     "in_stock_total": 4,
            #     "qty_in_strip": 1,
            #     "added_on": "2021-03-08T17:21:50.448572Z",
            #     "medicine_detail":
            #         [
            #             {
            #                 "salt_name": "jjjjjjjj",
            #                 "salt_qty": "66",
            #                 "salt_qty_type": "Frree",
            #                 "description": " worn in feel. Retains color, shape and softness. Machine wash cold. Use only non-chlorine bleach when needed. Tumble dry low. Do",
            #                 "added_on": "2020-02-03"
            #             },
            #             {
            #                 "salt_name": "jjjjjjjj",
            #                 "salt_qty": "66",
            #                 "salt_qty_type": "Frree",
            #                 "description": " worn in feel. Retains color, shape and softness. Machine wash cold. Use only non-chlorine bleach when needed. Tumble dry low. Do",
            #                 "added_on": "2020-02-03"
            #             },
            #             {
            #                 "salt_name": "jjjjjjjj",
            #                 "salt_qty": "66",
            #                 "salt_qty_type": "Frree",
            #                 "description": " worn in feel. Retains color, shape and softness. Machine wash cold. Use only non-chlorine bleach when needed. Tumble dry low. Do",
            #                 "added_on": "2020-02-03"
            #             }
            #         ]
            # }

        return Response(dict_response)

    def retrieve(self,request, pk=None):
        queryset = Medicine.objects.all()
        medicine = get_object_or_404(queryset, pk=pk)
        serializer = MedicineSerializer(medicine, context={"request": request})
        medicine_serializer_data = serializer.data


        medicine_details = MedicalDetails.objects.filter(medicine_id=medicine_serializer_data["id"])
        medicine_detail_serializers = MedicalDetailsSerializerSimple(medicine_details, many=True)
        medicine_serializer_data['medicine_details'] = medicine_detail_serializers.data

        return Response({"error": False, "message": "medicine single data fetch", "data": medicine_serializer_data })

    def update(self, request, pk=None):
        queryset = Medicine.objects.all()
        medicine = get_object_or_404(queryset,pk=pk)
        serializer = MedicineSerializer(medicine, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"error":False, "message":"medicine data is updated successfully"})

class JoinMedicalDetailsViewSet(viewsets.ViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        medical_details = MedicalDetails.objects.all().select_related('medicine_id', 'medicine_id__company_id')
        serializer = JoinMedicalDetailsSerializer(medical_details, many=True)

        return Response(serializer.data)


class ReverseMedicalDetailsViewSet(viewsets.ViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        # company = Company.objects.all().prefetch_related('medicines')
        company = Company.objects.all().prefetch_related(Prefetch('medicines', queryset=Medicine.objects.all().prefetch_related('medical_detailss')))
        serializer = ReverseCompanySerializer(company, many=True)

        return Response(serializer.data)



company_list = CompanyViewSet.as_view({"get": "list"})
company_create = CompanyViewSet.as_view({"post": "create"})
company_update = CompanyViewSet.as_view({"put": "update"})

# join_medical_detail = JoinMedicalDetailsViewSet.as_view({"get": "list"})
