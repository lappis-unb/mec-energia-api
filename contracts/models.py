from django.db import models, transaction
from django.core.exceptions import ObjectDoesNotExist
from datetime import date, datetime

from utils.subgroup_util import Subgroup
from utils.date_util import DateUtils
from utils.energy_bill_util import EnergyBillUtils

from django.core.validators import FileExtensionValidator


class ContractManager(models.Manager):
    def create(self, *args, **kwargs):
        with transaction.atomic():
            try:
                obj = self.model(*args, **kwargs)

                obj.check_start_date_create_contract()
                obj.save()

                obj.set_last_contract_end_date()
            except Exception as e:
                raise e
            
            return obj


class Contract(models.Model):
    objects = ContractManager()

    def save(self, *args, **kwargs):
        self.subgroup = Subgroup.get_subgroup(self.supply_voltage)
        super().save(*args, **kwargs)

    tariff_flag_choices = (
        ('G', 'Verde'),
        ('B', 'Azul'),
    )

    consumer_unit = models.ForeignKey(
        'universities.ConsumerUnit',
        on_delete=models.PROTECT
    )

    distributor = models.ForeignKey(
        'tariffs.Distributor',
        related_name='contracts',
        on_delete=models.PROTECT,
    )

    start_date = models.DateField(
        default=date.today,
        null=False,
        blank=False
    )

    end_date = models.DateField(
        null=True,
        blank=True
    )

    tariff_flag = models.CharField(
        choices=tariff_flag_choices,
        max_length=1,
        null=True,
        blank=True
    )

    subgroup = models.CharField(
        max_length=3,
        null=True,
        blank=True
    )

    supply_voltage = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=False,
        blank=False
    )

    peak_contracted_demand_in_kw = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )

    off_peak_contracted_demand_in_kw = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )

    def check_start_date_create_contract(self):
        if self.consumer_unit.current_contract:
            if self.start_date <= self.consumer_unit.current_contract.start_date:
                raise Exception(self.start_date, self.consumer_unit.current_contract.start_date, 'Novo Contrato não pode ter uma data anterior ou igual ao Contrato atual')

    def check_start_date_edit_contract(self):
        if self.consumer_unit.previous_contract:
            if self.consumer_unit.previous_contract != self.consumer_unit.current_contract:
                if self.start_date < self.consumer_unit.previous_contract.start_date:
                    raise Exception('Contrato não pode ser editado com a data anterior ao ultimo Contrato')

    def check_start_date_is_valid(self):
        if self.end_date:
            return

        consumer_unit = self.consumer_unit

        if consumer_unit.current_contract:
            if self.start_date >= consumer_unit.oldest_contract.start_date and self.start_date < consumer_unit.current_contract.start_date:
                raise Exception('Already have the contract in this date')

    def check_tariff_flag_is_valid(self):
        if self.tariff_flag == 'G' and self.subgroup in ('A2', 'A3'):
            raise Exception(
                'Contrato não pode ter tensão equivalente aos subgrupos A2 ou A3 e ser modalidade Verde')

    def set_last_contract_end_date(self):
        day_before_start_date = DateUtils.get_yesterday_date(self.start_date)

        if self.consumer_unit.previous_contract:
            previous_contract = self.consumer_unit.previous_contract
            previous_contract.end_date = day_before_start_date
            previous_contract.save()

    def get_distributor_name(self):
        return self.distributor.name


class EnergyBill(models.Model):
    def save(self, *args, **kwargs):
        if not isinstance(self.date, date):
            try:
                self.date = datetime.strptime(self.date, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError(
                    "Invalid date format. Please use 'YYYY-MM-DD'.")
        if self.date > date.today():
            raise Exception(
                "Energy bill data cannot be later than current data.")

        if self.date < self.consumer_unit.oldest_contract.start_date:
            raise Exception(
                "Energy Bill date cannot be earlier than the oldest contract start date.")

        if not EnergyBillUtils.check_valid_consumption_demand(self):
            raise Exception('Consumption and demand field cannot be 0.')

        super().save(*args, **kwargs)

    contract = models.ForeignKey(
        'Contract',
        on_delete=models.PROTECT
    )

    consumer_unit = models.ForeignKey(
        'universities.ConsumerUnit',
        on_delete=models.PROTECT
    )

    date = models.DateField(
        null=True,
        blank=True
    )

    invoice_in_reais = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )

    is_atypical = models.BooleanField(
        default=False
    )

    peak_consumption_in_kwh = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )

    off_peak_consumption_in_kwh = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )

    peak_measured_demand_in_kw = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )

    off_peak_measured_demand_in_kw = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )

    energy_bill_file = models.FileField(
        validators=[
            FileExtensionValidator(allowed_extensions=[
                                   'pdf', 'doc', 'ppt', 'xlsx', 'png', 'jpg', 'jpeg'])
        ],
        max_length=None,
        null=True,
        blank=True,
    )

    anotacoes = models.TextField(  # Novo campo de anotações
        null=True,
        blank=True,
    )

    address = models.TextField(
        null=True,
        blank=True
    )

    @classmethod
    def get_energy_bill(cls, consumer_unit_id, month, year):
        try:
            energy_bill = cls.objects.get(
                consumer_unit=consumer_unit_id,
                date__month=month,
                date__year=year)

            return energy_bill
        except ObjectDoesNotExist:
            return None
        except Exception as error:
            raise Exception('Get Energy Bill: ' + str(error))

    def check_energy_bill_month_year(consumer_unit_id, date):
        has_already_energy_bill = EnergyBill.objects.filter(
            consumer_unit=consumer_unit_id,
            date__year=date.year,
            date__month=date.month).exists()

        if has_already_energy_bill:
            return True
        else:
            return False

    def check_energy_bill_covered_by_contract(consumer_unit_id, date):
        oldest_contract = Contract.objects.filter(
            consumer_unit=consumer_unit_id
        ).order_by('start_date').first()

        latest_contract = Contract.objects.filter(
            consumer_unit=consumer_unit_id
        ).order_by('-start_date').first()

        if oldest_contract and latest_contract:
            if date >= oldest_contract.start_date or date >= latest_contract.start_date:
                return True

        return False
