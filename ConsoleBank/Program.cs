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
            Application.SetCompatibleTextRenderingDefault(false);
            servis = new BankovskiyServis(ObrabotatOperaciyu);
            servis.ZagruzitBazu();
            BankDialogi.Info("Добро пожаловать в консольный банк");

            while (true)
            {
                PokazatMenu();
                string vybor = Console.ReadLine();
                if (vybor == "0")
                {
                    if (Vyhod())
                        break;
                    continue;
                }
                if (vybor == "1") Registraciya();
                else if (vybor == "2") Vhod();
                else if (vybor == "3") Balans();
                else if (vybor == "4") Popolnit();
                else if (vybor == "5") Snyat();
                else if (vybor == "6") Perevod();
                else if (vybor == "7") DialogZagruzka();
                else if (vybor == "8") DialogSohranenie();
                else if (vybor == "9") Sverka();
                else
                {
                    BankDialogi.Oshibka("Нет такого пункта меню");
                }
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
            Console.WriteLine("9. Сверка");
            Console.WriteLine("0. Выход");
            Console.Write("Выберите пункт: ");
        }

        static void PokazatRezultat(string text)
        {
            Console.WriteLine(text);
            if (text.Contains("не") || text.Contains("Недостаточно") || text.Contains("отмен"))
                BankDialogi.Oshibka(text);
            else if (text.Contains("Сначала"))
                BankDialogi.Preduprezhdenie(text);
            else
                BankDialogi.Info(text);
        }

        static bool Vyhod()
        {
            if (BankDialogi.DaNet("Сохранить данные и выйти?"))
            {
                servis.SohranitBazu();
                BankDialogi.Info("До свидания");
                return true;
            }
            if (BankDialogi.DaNet("Выйти без сохранения?"))
            {
                BankDialogi.Info("До свидания");
                return true;
            }
            BankDialogi.Preduprezhdenie("Выход отменен");
            return false;
        }

        static void Registraciya()
        {
            Console.Write("Логин: ");
            string login = Console.ReadLine();
            Console.Write("Пароль: ");
            string parol = Console.ReadLine();
            PokazatRezultat(servis.Registraciya(login, parol));
        }

        static void Vhod()
        {
            Console.Write("Логин: ");
            string login = Console.ReadLine();
            Console.Write("Пароль: ");
            string parol = Console.ReadLine();
            PokazatRezultat(servis.Vhod(login, parol));
        }

        static void Balans()
        {
            string text = servis.PoluchitBalans();
            PokazatRezultat(text);
        }

        static decimal ChitatSummu()
        {
            Console.Write("Сумма: ");
            string s = Console.ReadLine();
            decimal sum;
            if (!decimal.TryParse(s, out sum))
            {
                BankDialogi.Oshibka("Введите число");
                return -1;
            }
            return sum;
        }

        static void Popolnit()
        {
            decimal sum = ChitatSummu();
            if (sum <= 0) return;
            if (BankDialogi.DaNet("Пополнить счет на " + sum + " руб.?"))
                PokazatRezultat(servis.Popolnit(sum));
        }

        static void Snyat()
        {
            decimal sum = ChitatSummu();
            if (sum <= 0) return;
            if (BankDialogi.DaNet("Снять " + sum + " руб.?"))
                PokazatRezultat(servis.Snyat(sum));
        }

        static void Perevod()
        {
            Console.Write("Логин получателя: ");
            string login = Console.ReadLine();
            decimal sum = ChitatSummu();
            if (sum <= 0) return;
            if (BankDialogi.DaNet("Перевести " + sum + " руб. клиенту " + login + "?"))
                PokazatRezultat(servis.Perevod(login, sum));
        }

        static void DialogZagruzka()
        {
            string text = servis.ZagruzitIzDialoga();
            Console.WriteLine(text);
            if (text.Contains("отмен"))
                BankDialogi.Preduprezhdenie(text);
        }

        static void DialogSohranenie()
        {
            string text = servis.SohranitVDialog();
            Console.WriteLine(text);
            if (text.Contains("отмен"))
                BankDialogi.Preduprezhdenie(text);
        }

        static void Sverka()
        {
            servis.SdelatSverku();
            BankDialogi.Info("Сверка завершена. Смотрите консоль.");
        }
    }
}
