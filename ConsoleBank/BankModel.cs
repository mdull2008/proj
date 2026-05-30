using System;
using System.Collections.Generic;
using System.IO;
using System.Windows.Forms;

namespace ConsoleBank
{
    class OperaciyaInfo : EventArgs
    {
        public string Tekst;
    }

    class Klient
    {
        public event EventHandler<OperaciyaInfo> Operaciya;

        public string Login;
        public string Parol;
        public decimal Balans;

        void Soobshit(string text)
        {
            if (Operaciya != null)
                Operaciya(this, new OperaciyaInfo { Tekst = text });
        }

        public void Popolnit(decimal summa)
        {
            Balans += summa;
            Soobshit("Пополнение на " + summa + " руб. Баланс: " + Balans);
        }

        public bool Snyat(decimal summa)
        {
            if (summa > Balans)
                return false;
            Balans -= summa;
            Soobshit("Снятие " + summa + " руб. Баланс: " + Balans);
            return true;
        }

        public bool Perevesti(Klient komu, decimal summa)
        {
            if (summa > Balans)
                return false;
            Balans -= summa;
            komu.Balans += summa;
            Soobshit("Перевод " + summa + " руб. клиенту " + komu.Login);
            komu.Soobshit("Получен перевод " + summa + " руб. от " + Login);
            return true;
        }
    }

    class SpisokKlientov<T> where T : Klient
    {
        List<T> spisok = new List<T>();

        public void Dobavit(T klient)
        {
            spisok.Add(klient);
        }

        public void Ochistit()
        {
            spisok.Clear();
        }

        public bool Est(string login)
        {
            foreach (T k in spisok)
            {
                if (k.Login == login)
                    return true;
            }
            return false;
        }

        public T Nayti(string login)
        {
            foreach (T k in spisok)
            {
                if (k.Login == login)
                    return k;
            }
            return null;
        }

        public List<T> Vse()
        {
            return spisok;
        }
    }

    class BankovskiyFayl
    {
        string put;

        public BankovskiyFayl(string imyaFayla)
        {
            put = imyaFayla;
        }

        public bool EstFayl()
        {
            return File.Exists(put);
        }

        public void Sohranit(SpisokKlientov<Klient> baza)
        {
            List<string> stroki = new List<string>();
            foreach (Klient k in baza.Vse())
            {
                string stroka = k.Login + ";" + k.Parol + ";" + k.Balans;
                stroki.Add(stroka);
            }
            File.WriteAllLines(put, stroki);
        }

        public void Zagruzit(SpisokKlientov<Klient> baza)
        {
            if (!File.Exists(put))
                return;
            string[] stroki = File.ReadAllLines(put);
            foreach (string s in stroki)
            {
                if (s == "")
                    continue;
                string[] chasti = s.Split(';');
                if (chasti.Length < 3)
                    continue;
                decimal balans = 0;
                decimal.TryParse(chasti[2], out balans);
                Klient k = new Klient();
                k.Login = chasti[0];
                k.Parol = chasti[1];
                k.Balans = balans;
                baza.Dobavit(k);
            }
        }
    }

    class EtapSverki
    {
        public void Proverit(SpisokKlientov<Klient> baza, string putFayla)
        {
            Console.WriteLine();
            Console.WriteLine("========== СВЕРКА ==========");

            decimal summaPam = 0;
            foreach (Klient k in baza.Vse())
                summaPam += k.Balans;

            Console.WriteLine("В памяти программы:");
            foreach (Klient k in baza.Vse())
                Console.WriteLine("  " + k.Login + " - " + k.Balans + " руб.");
            Console.WriteLine("Клиентов: " + baza.Vse().Count);
            Console.WriteLine("Сумма балансов: " + summaPam + " руб.");

            if (!File.Exists(putFayla))
            {
                Console.WriteLine("Файл " + putFayla + " не найден");
                Console.WriteLine("============================");
                return;
            }

            SpisokKlientov<Klient> izFayla = new SpisokKlientov<Klient>();
            BankovskiyFayl f = new BankovskiyFayl(putFayla);
            f.Zagruzit(izFayla);

            decimal summaFayl = 0;
            foreach (Klient k in izFayla.Vse())
                summaFayl += k.Balans;

            Console.WriteLine();
            Console.WriteLine("В файле " + putFayla + ":");
            foreach (Klient k in izFayla.Vse())
                Console.WriteLine("  " + k.Login + " - " + k.Balans + " руб.");
            Console.WriteLine("Клиентов: " + izFayla.Vse().Count);
            Console.WriteLine("Сумма балансов: " + summaFayl + " руб.");

            bool vseOk = true;
            if (baza.Vse().Count != izFayla.Vse().Count)
                vseOk = false;

            foreach (Klient k in baza.Vse())
            {
                Klient vFayle = izFayla.Nayti(k.Login);
                if (vFayle == null)
                {
                    Console.WriteLine("Нет в файле: " + k.Login);
                    vseOk = false;
                }
                else if (vFayle.Balans != k.Balans)
                {
                    Console.WriteLine("Разный баланс: " + k.Login);
                    vseOk = false;
                }
            }

            foreach (Klient k in izFayla.Vse())
            {
                if (!baza.Est(k.Login))
                {
                    Console.WriteLine("Лишний в файле: " + k.Login);
                    vseOk = false;
                }
            }

            Console.WriteLine();
            if (vseOk)
                Console.WriteLine("Итог сверки: данные совпадают");
            else
                Console.WriteLine("Итог сверки: найдены отличия");
            Console.WriteLine("============================");
        }
    }

    class BankFaylDialog
    {
        public bool ZagruzitCherezDialog(SpisokKlientov<Klient> baza)
        {
            OpenFileDialog otkrit = new OpenFileDialog();
            otkrit.Filter = "Файл банка (*.txt)|*.txt";
            otkrit.Title = "Открыть базу клиентов";
            if (otkrit.ShowDialog() != DialogResult.OK)
                return false;
            baza.Ochistit();
            string[] stroki = File.ReadAllLines(otkrit.FileName);
            foreach (string s in stroki)
            {
                if (s == "")
                    continue;
                string[] chasti = s.Split(';');
                if (chasti.Length < 3)
                    continue;
                decimal balans = 0;
                decimal.TryParse(chasti[2], out balans);
                Klient k = new Klient();
                k.Login = chasti[0];
                k.Parol = chasti[1];
                k.Balans = balans;
                baza.Dobavit(k);
            }
            return true;
        }

        public bool SohranitCherezDialog(SpisokKlientov<Klient> baza)
        {
            SaveFileDialog sohranit = new SaveFileDialog();
            sohranit.Filter = "Файл банка (*.txt)|*.txt";
            sohranit.Title = "Сохранить базу клиентов";
            sohranit.FileName = "bank.txt";
            if (sohranit.ShowDialog() != DialogResult.OK)
                return false;
            List<string> stroki = new List<string>();
            foreach (Klient k in baza.Vse())
            {
                stroki.Add(k.Login + ";" + k.Parol + ";" + k.Balans);
            }
            File.WriteAllLines(sohranit.FileName, stroki);
            return true;
        }
    }
}
