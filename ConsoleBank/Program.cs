using System;
using System.Windows.Forms;

namespace ConsoleBank
{
    class Program
    {
        static BankovskiyServis servis;

        [STAThread]
        static void Main(string[] args)
        {
            Application.EnableVisualStyles();
            servis = new BankovskiyServis(ObrabotatOperaciyu);
            servis.ZagruzitBazu();

            while (true)
            {
                PokazatMenu();
                string vybor = Console.ReadLine();
                if (vybor == "0")
                {
                    servis.SohranitBazu();
                    Console.WriteLine("До свидания");
                    break;
                }
                if (vybor == "1") Registraciya();
                else if (vybor == "2") Vhod();
                else if (vybor == "3") Balans();
                else if (vybor == "4") Popolnit();
                else if (vybor == "5") Snyat();
                else if (vybor == "6") Perevod();
                else if (vybor == "7") DialogZagruzka();
                else if (vybor == "8") DialogSohranenie();
                else if (vybor == "9") servis.SdelatSverku();
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
            if (servis.Tekushiy != null)
                Console.WriteLine("Клиент: " + servis.Tekushiy.Login);
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
            Console.Write("Пароль: ");
            string parol = Console.ReadLine();
            Console.WriteLine(servis.Registraciya(login, parol));
        }

        static void Vhod()
        {
            Console.Write("Логин: ");
            string login = Console.ReadLine();
            Console.Write("Пароль: ");
            string parol = Console.ReadLine();
            Console.WriteLine(servis.Vhod(login, parol));
        }

        static void Balans()
        {
            Console.WriteLine(servis.PoluchitBalans());
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
            decimal sum = ChitatSummu();
            if (sum <= 0) return;
            Console.WriteLine(servis.Popolnit(sum));
        }

        static void Snyat()
        {
            decimal sum = ChitatSummu();
            if (sum <= 0) return;
            Console.WriteLine(servis.Snyat(sum));
        }

        static void Perevod()
        {
            Console.Write("Логин получателя: ");
            string login = Console.ReadLine();
            decimal sum = ChitatSummu();
            if (sum <= 0) return;
            Console.WriteLine(servis.Perevod(login, sum));
        }

        static void DialogZagruzka()
        {
            Console.WriteLine(servis.ZagruzitIzDialoga());
        }

        static void DialogSohranenie()
        {
            Console.WriteLine(servis.SohranitVDialog());
        }
    }
}
