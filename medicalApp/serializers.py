from rest_framework import serializers

from .models import Company, CompanyBank, Medicine, MedicalDetails, Employee, Customer, Bill, \
    CustomerRequest, CompanyAccount, EmployeeBank, EmployeeSalary, BillDetails


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model=Company
        fields= ["name", "address"]


class CompanyBankSerializer(serializers.ModelSerializer):
    class Meta:
        model=CompanyBank
        fields=["id", "bank_account_no", "company_id"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['company'] = CompanySerializer(instance.company_id).data
        return response


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model=Medicine
        fields="__all__"

    def to_representation(self, instance):
        response=super().to_representation(instance)
        response['company']=CompanySerializer(instance.company_id).data
        return response



class MedicalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=MedicalDetails
        fields="__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['medicine'] = MedicineSerializer(instance.medicine_id).data
        return response

class MedicalDetailsSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model=MedicalDetails
        fields="__all__"

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        fields="__all__"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields="__all__"

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bill
        fields="__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['customer'] = CustomerSerializer(instance.customer_id).data
        return response

class CustomerRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomerRequest
        fields="__all__"


class CompanyAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=CompanyAccount
        fields="__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['company'] = CompanySerializer(instance.company_id).data
        return response


class EmployeeBankSerializer(serializers.ModelSerializer):
    class Meta:
        model=EmployeeBank
        fields="__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['employee'] = EmployeeSerializer(instance.employee_id).data
        return response


class EmployeeSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model=EmployeeSalary
        fields="__all__"

class BillDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=BillDetails
        fields="__all__"


##############################################################

class JoinCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = "__all__"

class JoinMedicineSerializer(serializers.ModelSerializer):
    company_id = JoinCompanySerializer()

    class Meta:
        model = Medicine
        fields = "__all__"

class JoinMedicalDetailsSerializer(serializers.ModelSerializer):
    medicine_id = JoinMedicineSerializer()

    class Meta:
        model=MedicalDetails
        fields="__all__"


##############################################################

class ReverseMedicalDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model=MedicalDetails
        fields="__all__"


class ReverseMedicineSerializer(serializers.ModelSerializer):
    medical_detai = ReverseMedicalDetailsSerializer(source='medical_detailss', many=True)

    class Meta:
        model = Medicine
        fields = "__all__"


class ReverseCompanySerializer(serializers.ModelSerializer):
    medici = ReverseMedicineSerializer(source='medicines', many=True)

    class Meta:
        model = Company
        fields = "__all__"
