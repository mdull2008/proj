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

    class Program
    {
        static SpisokKlientov<Klient> baza = new SpisokKlientov<Klient>();
        static BankovskiyFayl fayl = new BankovskiyFayl("bank.txt");
        static BankFaylDialog dialog = new BankFaylDialog();
        static EtapSverki sverka = new EtapSverki();
        static Klient tekushiy = null;

        [STAThread]
        static void Main(string[] args)
        {
            Application.EnableVisualStyles();
            ZagruzitBazu();

            while (true)
            {
                PokazatMenu();
                string vybor = Console.ReadLine();
                if (vybor == "0")
                {
                    SohranitBazu();
                    Console.WriteLine("До свидания");
                    break;
                }
                if (vybor == "1") Registraciya();
                else if (vybor == "2") Vhod();
                else if (vybor == "3") Balans();
                else if (vybor == "4") Popolnit();
                else if (vybor == "5") Snyat();
                else if (vybor == "6") Perevod();
                else if (vybor == "7") ZagruzitIzFayla();
                else if (vybor == "8") SohranitVFayl();
                else if (vybor == "9") SdelatSverku();
                else Console.WriteLine("Нет такого пункта");
            }
        }

        static void ZagruzitBazu()
        {
            baza.Ochistit();
            if (fayl.EstFayl())
            {
                fayl.Zagruzit(baza);
            }
            else
            {
                baza.Dobavit(new Klient { Login = "admin", Parol = "admin", Balans = 10000 });
                baza.Dobavit(new Klient { Login = "madina", Parol = "madina", Balans = 5000 });
                fayl.Sohranit(baza);
            }
            foreach (Klient k in baza.Vse())
                k.Operaciya += ObrabotatOperaciyu;
        }

        static void SohranitBazu()
        {
            fayl.Sohranit(baza);
        }

        static void ObrabotatOperaciyu(object otpravitel, OperaciyaInfo e)
        {
            Console.WriteLine("[событие] " + e.Tekst);
        }

        static void PokazatMenu()
        {
            Console.WriteLine();
            Console.WriteLine("===== КОНСОЛЬНЫЙ БАНК =====");
            if (tekushiy != null)
                Console.WriteLine("Клиент: " + tekushiy.Login);
            Console.WriteLine("1. Регистрация");
            Console.WriteLine("2. Вход");
            Console.WriteLine("3. Баланс");
            Console.WriteLine("4. Пополнить счет");
            Console.WriteLine("5. Снять деньги");
            Console.WriteLine("6. Перевод");
            Console.WriteLine("7. Открыть файл (OpenFileDialog)");
            Console.WriteLine("8. Сохранить файл (SaveFileDialog)");
            Console.WriteLine("9. Сверка (память и bank.txt)");
            Console.WriteLine("0. Выход");
            Console.Write("Выберите пункт: ");
        }

        static void Registraciya()
        {
            Console.Write("Логин: ");
            string login = Console.ReadLine();
            if (login == "" || baza.Est(login))
            {
                Console.WriteLine("Логин занят или пустой");
                return;
            }
            Console.Write("Пароль: ");
            string parol = Console.ReadLine();
            Klient noviy = new Klient { Login = login, Parol = parol, Balans = 0 };
            noviy.Operaciya += ObrabotatOperaciyu;
            baza.Dobavit(noviy);
            SohranitBazu();
            Console.WriteLine("Счет создан");
        }

        static void Vhod()
        {
            Console.Write("Логин: ");
            string login = Console.ReadLine();
            Console.Write("Пароль: ");
            string parol = Console.ReadLine();
            Klient k = baza.Nayti(login);
            if (k == null)
            {
                Console.WriteLine("Пользователь не найден");
                return;
            }
            if (k.Parol != parol)
            {
                Console.WriteLine("Неверный пароль");
                return;
            }
            tekushiy = k;
            Console.WriteLine("Вы вошли в систему");
        }

        static bool ProveritVhod()
        {
            if (tekushiy == null)
            {
                Console.WriteLine("Сначала войдите в систему");
                return false;
            }
            return true;
        }

        static void Balans()
        {
            if (!ProveritVhod()) return;
            Console.WriteLine("Баланс: " + tekushiy.Balans + " руб.");
        }

        static decimal ChitatSummu()
        {
            Console.Write("Сумма: ");
            string s = Console.ReadLine();
            decimal sum;
            if (!decimal.TryParse(s, out sum))
            {
                Console.WriteLine("Введите число");
                return -1;
            }
            return sum;
        }

        static void Popolnit()
        {
            if (!ProveritVhod()) return;
            decimal sum = ChitatSummu();
            if (sum <= 0) return;
            tekushiy.Popolnit(sum);
            SohranitBazu();
        }

        static void Snyat()
        {
            if (!ProveritVhod()) return;
            decimal sum = ChitatSummu();
            if (sum <= 0) return;
            if (!tekushiy.Snyat(sum))
                Console.WriteLine("Недостаточно средств");
            else
                SohranitBazu();
        }

        static void PodpisatSobytiya()
        {
            foreach (Klient k in baza.Vse())
                k.Operaciya += ObrabotatOperaciyu;
        }

        static void ZagruzitIzFayla()
        {
            if (dialog.ZagruzitCherezDialog(baza))
            {
                tekushiy = null;
                PodpisatSobytiya();
                Console.WriteLine("База загружена");
            }
        }

        static void SohranitVFayl()
        {
            if (dialog.SohranitCherezDialog(baza))
                Console.WriteLine("База сохранена");
        }

        static void SdelatSverku()
        {
            sverka.Proverit(baza, "bank.txt");
        }

        static void Perevod()
        {
            if (!ProveritVhod()) return;
            Console.Write("Логин получателя: ");
            string login = Console.ReadLine();
            Klient komu = baza.Nayti(login);
            if (komu == null)
            {
                Console.WriteLine("Получатель не найден");
                return;
            }
            if (komu.Login == tekushiy.Login)
            {
                Console.WriteLine("Нельзя перевести себе");
                return;
            }
            decimal sum = ChitatSummu();
            if (sum <= 0) return;
            if (!tekushiy.Perevesti(komu, sum))
                Console.WriteLine("Недостаточно средств");
            else
                SohranitBazu();
        }
    }
}
