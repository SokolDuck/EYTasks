from django.db import models

# Create your models here.

class Classes(models.Model):
    Id = models.IntegerField(primary_key=True, unique=True, auto_created=True)
    Code = models.IntegerField(unique=True)
    Description = models.CharField(max_length=200)

    def __str__(self):
        return "<code: %d, Descr: %s>" %\
                (self.Code,
                self.Description)


class BalanceAccounts(models.Model):
    Id = models.IntegerField(primary_key=True, unique=True, auto_created=True)
    ClassId = models.ForeignKey(Classes, on_delete=models.CASCADE)
    BalanceAccountNumber = models.IntegerField(name='Number', unique=True)

    def __str__(self):
        return "<num: %d>" % (self.Number)

class Currency(models.Model):
    Id = models.IntegerField(primary_key=True, unique=True, auto_created=True)
    Name = models.CharField(max_length=50)

    def __str__(self):
        return 'id: %d name: %s' % (self.Id, self.Name)

class Files(models.Model):
    Id = models.IntegerField(primary_key=True, unique=True, auto_created=True)
    Name = models.CharField(max_length=200)
    DateSince = models.DateField(name='date_since')
    DateTo = models.DateField(name='date_to')
    BanksName = models.CharField(max_length=100)
    CurrencyId = models.ForeignKey(Currency, on_delete=models.CASCADE)

    def __str__(self):
        return "<Id: %d,Name: %s, DS: %s, DT: %s, Bank: %s>" %\
                (self.Id,
                self.Name,
                self.date_since.__str__(),
                self.date_to.__str__(),
                self.BanksName)

class Records(models.Model):
    Id = models.IntegerField(primary_key=True, unique=True, auto_created=True)
    FileId = models.ForeignKey(Files, on_delete=models.CASCADE)
    BalanceAccountsId = models.ForeignKey(BalanceAccounts, on_delete=models.CASCADE)
    BalanceOfInputAssets = models.FloatField()
    BalanceOfOutputAssets = models.FloatField()
    BalanceOfInputLiabilities = models.FloatField()
    BalanceOfOutputLiabilities = models.FloatField()
    CashFlowDebit = models.FloatField()
    CashFlowCredit = models.FloatField()

    def __add__(self,s ):
        self.BalanceOfOutputLiabilities += s.BalanceOfOutputLiabilities
        self.BalanceOfInputAssets += s.BalanceOfInputAssets
        self.BalanceOfInputLiabilities += s.BalanceOfInputLiabilities
        self.BalanceOfOutputAssets += s.BalanceOfOutputAssets
        self.CashFlowCredit += s.CashFlowCredit
        self.CashFlowDebit += s.CashFlowDebit
        return self

    def getZerous(self):
        self.BalanceOfInputAssets = 0.0
        self.BalanceOfInputLiabilities = 0.0
        self.CashFlowDebit = 0.0
        self.CashFlowCredit = 0.0
        self.BalanceOfOutputAssets = 0.0
        self.BalanceOfOutputLiabilities = 0.0
        return self

    def getList(self):
        return [
            self.BalanceOfInputAssets,
            self.BalanceOfInputLiabilities,
            self.CashFlowDebit,
            self.CashFlowCredit,
            self.BalanceOfOutputAssets,
            self.BalanceOfOutputLiabilities]

    def __str__(self):
        return "<1: %f, 2: %f, 3: %f, 4: %f, 5: %f, 6: %f>" % \
                ( 
                self.BalanceOfInputAssets,
                self.BalanceOfInputLiabilities,
                self.CashFlowDebit,
                self.CashFlowCredit,
                self.BalanceOfOutputAssets,
                self.BalanceOfOutputLiabilities)
