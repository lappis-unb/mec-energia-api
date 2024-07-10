
TariffsNotFoundError = (1, "Lance as tarifas para realizar a análise")
NotEnoughEnergyBills = (2, "Lance ao menos %d faturas para realizar a análise")
NotEnoughEnergyBillsWithAtypical = (3, NotEnoughEnergyBills[1] + f".{chr(10)}Somente faturas marcadas como {chr(34)}incluir na análise{chr(34)} são consideradas.")
PendingBillsWarnning = (4, "Lance mais %d %s dos últimos 12 meses para aumentar a precisão da análise")
ExpiredTariffWarnning = (5, "Atualize as tarifas vencidas para aumentar a precisão da análise")
DuplicatedDateError = (6, "Este mês está duplicado na planilha")
DateNotCoverByContractError = (7, "Este mês não é coberto por um contrato registrado no sistema")
FormatDateError = (8, "A data não está formatada corretamente")
ValueMaxError = (9, "Valores de Consumo e Demanda devem ser números entre 0,1 e 99.999,99")
AlreadyHasEnergyBill = (10, "Já existe uma fatura lançada neste mês")

class ErrorMensageParser():    
    @classmethod
    def parse(cls, errorCode: tuple[int, str], subs = None):
        return (errorCode[0], errorCode[1]%subs)
