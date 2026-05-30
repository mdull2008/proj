using System;
using System.Collections.Generic;

namespace ConsoleBank
{
    class Klient
    {
        public string Login;
        public string Parol;
        public decimal Balans;
    }

    class Program
    {
        static Dictionary<string, Klient> baza = new Dictionary<string, Klient>();
        static Klient tekushiy = null;

        static void Main(string[] args)
        {
            baza["admin"] = new Klient { Login = "admin", Parol = "admin", Balans = 10000 };
            baza["madina"] = new Klient { Login = "madina", Parol = "madina", Balans = 5000 };

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
            if (login == "" || baza.ContainsKey(login))
            {
                Console.WriteLine("Логин занят или пустой");
                return;
            }
            Console.Write("Пароль: ");
            string parol = Console.ReadLine();
            baza[login] = new Klient { Login = login, Parol = parol, Balans = 0 };
            Console.WriteLine("Счет создан");
        }

        static void Vhod()
        {
            Console.Write("Логин: ");
            string login = Console.ReadLine();
            Console.Write("Пароль: ");
            string parol = Console.ReadLine();
            if (!baza.ContainsKey(login))
            {
                Console.WriteLine("Пользователь не найден");
                return;
            }
            if (baza[login].Parol != parol)
            {
                Console.WriteLine("Неверный пароль");
                return;
            }
            tekushiy = baza[login];
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
            tekushiy.Balans += sum;
            Console.WriteLine("Готово. Баланс: " + tekushiy.Balans);
        }

        static void Snyat()
        {
            if (!ProveritVhod()) return;
            decimal sum = ChitatSummu();
            if (sum <= 0) return;
            if (sum > tekushiy.Balans)
            {
                Console.WriteLine("Недостаточно средств");
                return;
            }
            tekushiy.Balans -= sum;
            Console.WriteLine("Готово. Баланс: " + tekushiy.Balans);
        }

        static void Perevod()
        {
            if (!ProveritVhod()) return;
            Console.Write("Логин получателя: ");
            string komu = Console.ReadLine();
            if (!baza.ContainsKey(komu))
            {
                Console.WriteLine("Получатель не найден");
                return;
            }
            if (komu == tekushiy.Login)
            {
                Console.WriteLine("Нельзя перевести себе");
                return;
            }
            decimal sum = ChitatSummu();
            if (sum <= 0) return;
            if (sum > tekushiy.Balans)
            {
                Console.WriteLine("Недостаточно средств");
                return;
            }
            tekushiy.Balans -= sum;
            baza[komu].Balans += sum;
            Console.WriteLine("Перевод выполнен");
        }
    }
}
