from dataclasses import dataclass
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from datetime import date

from django.utils.translation import gettext_lazy as _

from universities.models import University, ConsumerUnit
from contracts.models import Contract

class Distributor(models.Model):
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )

    cnpj = models.CharField(
        max_length=14,
        verbose_name=_('CNPJ'),
        help_text=_('14 números sem caracteres especiais')
    )

    university = models.ForeignKey(
        University,
        on_delete=models.PROTECT,    
        null=False,
        blank=False,
    )

    is_active = models.BooleanField(
        default=True
    )

    is_in_new_resolution = models.BooleanField(
        default=True
    )

    class Meta:
        unique_together = ['university', 'cnpj']

    @property
    def consumer_units_count(self) -> int:
        return len(self.get_consumer_units())

    @property
    def pending_tariffs_count(self) -> int:
        count = 0

        subgroups = self.get_subgroups_pending()

        for subgroup in subgroups:
            if subgroup['pending'] == True:
                count += 1
        
        return count

    @property
    def is_pending(self):        
        return True if self.pending_tariffs_count else False

    @classmethod
    def get_distributors_pending(cls, university_id):
        distributors = Distributor.objects.filter(university = university_id)
        pending_distributors = distributors
        
        for distributor in distributors:
            if not distributor.is_pending:
                pending_distributors = pending_distributors.exclude(id = distributor.id)

        return pending_distributors

    def get_consumer_units(self):
        return ConsumerUnit.objects.filter(university_id = self.university.id, contract__distributor = self, contract__end_date__isnull = True)

    def get_consumer_units_by_subgroup(self, subgroup):
        return ConsumerUnit.objects.filter(
            university_id = self.university.id,
            contract__distributor = self,
            contract__end_date__isnull = True,
            contract__subgroup = subgroup
        )
        
    def get_subgroups(self):
        subgroups = []

        contracts = Contract.objects.filter(consumer_unit__university__id = self.university.id, distributor = self, end_date__isnull = True)

        for contract in contracts:
            if contract.subgroup not in subgroups:
                subgroups.append(contract.subgroup)

        return subgroups

    def get_consumer_units_separated_by_subgroup(self):
        subgroup_list = []

        subgroups = self.get_subgroups()

        for subgroup in subgroups:
            is_pending = self.check_subgroups_pending(subgroup)    

            sb = {'subgroup': subgroup, 'pending': is_pending, 'consumer_units': []}

            consumer_unit_by_subgroup = self.get_consumer_units_by_subgroup(sb['subgroup'])

            for unit in consumer_unit_by_subgroup:
                sb['consumer_units'].append({'id': unit.id, 'name': unit.name})

            subgroup_list.append(sb)

        return subgroup_list

    def get_subgroups_pending(self):
        subgroup_list = []

        subgroups = self.get_subgroups()

        for subgroup in subgroups:
            is_pending = self.check_subgroups_pending(subgroup)                  
            
            sb = {'subgroup': subgroup, 'pending': is_pending}
            subgroup_list.append(sb)

        return subgroup_list

    def check_subgroups_pending(self, subgroup):
        is_pending = False

        tariffs = Tariff.objects.filter(distributor = self, flag = Tariff.BLUE, subgroup = subgroup)

        for tariff in tariffs:
            if tariff.pending == True:
                is_pending = True
                break

        if not tariffs:
            is_pending = True

        return is_pending

    def get_tariffs_by_subgroups(self, request_subgroup):
        try:
            blue = Tariff.objects.get(distributor = self.id, subgroup = request_subgroup, flag = Tariff.BLUE)
            green = Tariff.objects.get(distributor = self.id, subgroup = request_subgroup, flag = Tariff.GREEN)

            return blue, green
        except ObjectDoesNotExist:
            return None, None
        except Exception as error:
            raise Exception({'error': str(error)})


class DataTariff:
    def is_blue(self):
        return type(self) == BlueTariff
    def is_green(self):
        return type(self) == GreenTariff
    def as_blue_tariff(self):
        if not self.is_blue():
            raise Exception('Tariff is green type. Cannot convert to blue')
        return self
    def as_green_tariff(self):
        if not self.is_green():
            raise Exception('Tariff is blue type. Cannot convert to green')
        return self

@dataclass
class BlueTariff(DataTariff):
    peak_tusd_in_reais_per_kw: float
    peak_tusd_in_reais_per_mwh: float
    peak_te_in_reais_per_mwh: float
    off_peak_tusd_in_reais_per_kw: float
    off_peak_tusd_in_reais_per_mwh: float
    off_peak_te_in_reais_per_mwh: float
    power_generation_tusd_in_reais_per_kw: float

@dataclass
class GreenTariff(DataTariff):
    peak_tusd_in_reais_per_mwh: float
    peak_te_in_reais_per_mwh: float
    off_peak_tusd_in_reais_per_mwh: float
    off_peak_te_in_reais_per_mwh: float
    na_tusd_in_reais_per_kw: float
    power_generation_tusd_in_reais_per_kw: float


class Tariff(models.Model):
    subgroups = (
        ('A1', '≥ 230 kV'),
        ('A2', 'de 88 kV a 138 kV'),
        ('A3', 'de 69 kV'),
        ('A3a', 'de 30 kV a 44 kV'),
        ('A4', 'de 2,3 kV a 25 kV'),
        ('AS', '< a 2,3 kV, a partir de sistema subterrâneo de distribuição'),
    )

    subgroup = models.CharField(
        choices=subgroups,
        max_length=3,
        null=False,
        blank=False,
    )

    distributor = models.ForeignKey(
        Distributor,
        related_name='tariffs',
        on_delete=models.CASCADE,    
        null=False,
        blank=False,
    )

    BLUE = 'B'
    GREEN = 'G'
    flag_options = (
        (BLUE, 'Azul'),
        (GREEN, 'Verde'),
    )

    # Não era pra esse campo ter um default. Mas makemigrations só ro
    # rodou assim. Era preferível que desse erro ao inserrir uma tarifa
    # sem opção de flag.
    flag = models.CharField(
        choices=flag_options,
        default=BLUE,
        max_length=1,
        null=False,
        blank=False,
    )

    class Meta:
        unique_together = ['subgroup', 'distributor', 'flag']

    start_date = models.DateField(
        null=False,
        blank=False,
    )

    end_date = models.DateField(
        null=False,
        blank=False,
    )

    @property
    def pending(self) -> bool:
        return self.end_date < date.today()

    peak_tusd_in_reais_per_kw = models.DecimalField(
        decimal_places=2,
        max_digits=6,
        null=True,
        blank=True,
    )
    peak_tusd_in_reais_per_mwh = models.DecimalField(
        decimal_places=2,
        max_digits=6,
        null=True,
        blank=True,
    )
    peak_te_in_reais_per_mwh = models.DecimalField(
        decimal_places=2,
        max_digits=6,
        null=True,
        blank=True,
    )
    off_peak_tusd_in_reais_per_kw = models.DecimalField(
        decimal_places=2,
        max_digits=6,
        null=True,
        blank=True,
    )
    off_peak_tusd_in_reais_per_mwh = models.DecimalField(
        decimal_places=2,
        max_digits=6,
        null=True,
        blank=True,
    )
    off_peak_te_in_reais_per_mwh = models.DecimalField(
        decimal_places=2,
        max_digits=6,
        null=True,
        blank=True,
    )
    na_tusd_in_reais_per_kw = models.DecimalField(
        decimal_places=2,
        max_digits=6,
        null=True,
        blank=True,
    )
    power_generation_tusd_in_reais_per_kw = models.DecimalField(
        decimal_places=2,
        max_digits=6,
        null=True,
        blank=True,
    )

    def is_blue(self) -> bool:
        return self.flag == Tariff.BLUE
    
    def is_green(self) -> bool:
        return self.flag == Tariff.GREEN

    def as_blue_tariff(self) -> BlueTariff:
        if not self.is_blue():
            raise Exception('Tariff is green type. Cannot convert to blue')
        return BlueTariff(
            peak_tusd_in_reais_per_kw=float(self.peak_tusd_in_reais_per_kw),
            peak_tusd_in_reais_per_mwh=float(self.peak_tusd_in_reais_per_mwh),
            peak_te_in_reais_per_mwh=float(self.peak_te_in_reais_per_mwh),
            off_peak_tusd_in_reais_per_kw=float(self.off_peak_tusd_in_reais_per_kw),
            off_peak_tusd_in_reais_per_mwh=float(self.off_peak_tusd_in_reais_per_mwh),
            off_peak_te_in_reais_per_mwh=float(self.off_peak_te_in_reais_per_mwh),
            power_generation_tusd_in_reais_per_kw=float(self.power_generation_tusd_in_reais_per_kw),
        )

    def as_green_tariff(self) -> GreenTariff:
        if self.is_blue():
            raise Exception('Tariff is blue type. Cannot convert to green')
        return GreenTariff(
            peak_tusd_in_reais_per_mwh=float(self.peak_tusd_in_reais_per_mwh),
            peak_te_in_reais_per_mwh=float(self.peak_te_in_reais_per_mwh),
            off_peak_tusd_in_reais_per_mwh=float(self.off_peak_tusd_in_reais_per_mwh),
            off_peak_te_in_reais_per_mwh=float(self.off_peak_te_in_reais_per_mwh),
            na_tusd_in_reais_per_kw=float(self.na_tusd_in_reais_per_kw),
            power_generation_tusd_in_reais_per_kw=float(self.power_generation_tusd_in_reais_per_kw),
        )


