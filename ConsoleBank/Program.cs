using System;
using System.Collections.Generic;

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

    class Program
    {
        static SpisokKlientov<Klient> baza = new SpisokKlientov<Klient>();
        static Klient tekushiy = null;

        static void Main(string[] args)
        {
            Klient admin = new Klient { Login = "admin", Parol = "admin", Balans = 10000 };
            Klient madina = new Klient { Login = "madina", Parol = "madina", Balans = 5000 };
            baza.Dobavit(admin);
            baza.Dobavit(madina);

            foreach (Klient k in baza.Vse())
                k.Operaciya += ObrabotatOperaciyu;

            while (true)
            {
                PokazatMenu();
                string vybor = Console.ReadLine();
                if (vybor == "0")
                {
                    Console.WriteLine("До свидания");
                    break;
                }
                if (vybor == "1") Registraciya();
                else if (vybor == "2") Vhod();
                else if (vybor == "3") Balans();
                else if (vybor == "4") Popolnit();
                else if (vybor == "5") Snyat();
                else if (vybor == "6") Perevod();
                else Console.WriteLine("Нет такого пункта");
            }
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
        }

        static void Snyat()
        {
            if (!ProveritVhod()) return;
            decimal sum = ChitatSummu();
            if (sum <= 0) return;
            if (!tekushiy.Snyat(sum))
                Console.WriteLine("Недостаточно средств");
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
        }
    }
}
