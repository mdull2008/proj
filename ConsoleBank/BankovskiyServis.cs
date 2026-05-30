using System;

namespace ConsoleBank
{
    class BankovskiyServis
    {
        public SpisokKlientov<Klient> Baza;
        public Klient Tekushiy;

        BankovskiyFayl fayl;
        BankFaylDialog dialog;
        EtapSverki sverka;
        EventHandler<OperaciyaInfo> obrabotchik;

        public BankovskiyServis(EventHandler<OperaciyaInfo> naSobytie)
        {
            Baza = new SpisokKlientov<Klient>();
            fayl = new BankovskiyFayl("bank.txt");
            dialog = new BankFaylDialog();
            sverka = new EtapSverki();
            obrabotchik = naSobytie;
            Tekushiy = null;
        }

        public void PodpisatSobytiya()
        {
            foreach (Klient k in Baza.Vse())
                k.Operaciya += obrabotchik;
        }

        public void ZagruzitBazu()
        {
            Baza.Ochistit();
            if (fayl.EstFayl())
                fayl.Zagruzit(Baza);
            else
            {
                Baza.Dobavit(new Klient { Login = "admin", Parol = "admin", Balans = 10000 });
                Baza.Dobavit(new Klient { Login = "madina", Parol = "madina", Balans = 5000 });
                fayl.Sohranit(Baza);
            }
            PodpisatSobytiya();
        }

        public void SohranitBazu()
        {
            fayl.Sohranit(Baza);
        }

        public string Registraciya(string login, string parol)
        {
            if (login == "" || Baza.Est(login))
                return "Логин занят или пустой";
            Klient noviy = new Klient { Login = login, Parol = parol, Balans = 0 };
            noviy.Operaciya += obrabotchik;
            Baza.Dobavit(noviy);
            SohranitBazu();
            return "Счет создан";
        }

        public string Vhod(string login, string parol)
        {
            Klient k = Baza.Nayti(login);
            if (k == null)
                return "Пользователь не найден";
            if (k.Parol != parol)
                return "Неверный пароль";
            Tekushiy = k;
            return "Вы вошли в систему";
        }

        public string PoluchitBalans()
        {
            if (Tekushiy == null)
                return "Сначала войдите в систему";
            return "Баланс: " + Tekushiy.Balans + " руб.";
        }

        public string Popolnit(decimal summa)
        {
            if (Tekushiy == null)
                return "Сначала войдите в систему";
            if (summa <= 0)
                return "Сумма должна быть больше нуля";
            Tekushiy.Popolnit(summa);
            SohranitBazu();
            return "Пополнение выполнено";
        }

        public string Snyat(decimal summa)
        {
            if (Tekushiy == null)
                return "Сначала войдите в систему";
            if (summa <= 0)
                return "Сумма должна быть больше нуля";
            if (!Tekushiy.Snyat(summa))
                return "Недостаточно средств";
            SohranitBazu();
            return "Снятие выполнено";
        }

        public string Perevod(string login, decimal summa)
        {
            if (Tekushiy == null)
                return "Сначала войдите в систему";
            Klient komu = Baza.Nayti(login);
            if (komu == null)
                return "Получатель не найден";
            if (komu.Login == Tekushiy.Login)
                return "Нельзя перевести себе";
            if (summa <= 0)
                return "Сумма должна быть больше нуля";
            if (!Tekushiy.Perevesti(komu, summa))
                return "Недостаточно средств";
            SohranitBazu();
            return "Перевод выполнен";
        }

        public string ZagruzitIzDialoga()
        {
            if (dialog.ZagruzitCherezDialog(Baza))
            {
                Tekushiy = null;
                PodpisatSobytiya();
                return "База загружена";
            }
            return "Загрузка отменена";
        }

        public string SohranitVDialog()
        {
            if (dialog.SohranitCherezDialog(Baza))
                return "База сохранена";
            return "Сохранение отменено";
        }

        public void SdelatSverku()
        {
            sverka.Proverit(Baza, "bank.txt");
        }
    }
}
