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
            BankDialogi.Privetstvie();

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
                else BankDialogi.NetPunktaMenu();
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

        static bool Vyhod()
        {
            if (BankDialogi.VyhodSohranit())
            {
                servis.SohranitBazu();
                BankDialogi.DoSvidaniya();
                return true;
            }
            if (BankDialogi.VyhodBezSohraneniya())
            {
                BankDialogi.DoSvidaniya();
                return true;
            }
            BankDialogi.VyhodOtmenen();
            return false;
        }

        static void Registraciya()
        {
            Console.Write("Логин: ");
            string login = Console.ReadLine();
            Console.Write("Пароль: ");
            string parol = Console.ReadLine();
            string rez = servis.Registraciya(login, parol);
            Console.WriteLine(rez);
            if (rez == "Счет создан")
                BankDialogi.SchetSozdan(login);
            else
                BankDialogi.LoginZanyat();
        }

        static void Vhod()
        {
            Console.Write("Логин: ");
            string login = Console.ReadLine();
            Console.Write("Пароль: ");
            string parol = Console.ReadLine();
            string rez = servis.Vhod(login, parol);
            Console.WriteLine(rez);
            if (rez == "Вы вошли в систему")
                BankDialogi.VhodUspeshno(login);
            else if (rez == "Пользователь не найден")
                BankDialogi.KlientNeNayden();
            else if (rez == "Неверный пароль")
                BankDialogi.NeverniyParol();
        }

        static void Balans()
        {
            string rez = servis.PoluchitBalans();
            Console.WriteLine(rez);
            if (rez == "Сначала войдите в систему")
                BankDialogi.NetVhoda();
            else if (servis.Tekushiy != null)
                BankDialogi.PokazatBalans(servis.Tekushiy.Balans);
        }

        static decimal ChitatSummu()
        {
            Console.Write("Сумма: ");
            string s = Console.ReadLine();
            decimal sum;
            if (!decimal.TryParse(s, out sum))
            {
                BankDialogi.NevernayaSumma();
                return -1;
            }
            return sum;
        }

        static void Popolnit()
        {
            if (servis.Tekushiy == null)
            {
                BankDialogi.NetVhoda();
                return;
            }
            decimal sum = ChitatSummu();
            if (sum <= 0)
            {
                BankDialogi.SummaNePodhodit();
                return;
            }
            if (!BankDialogi.PodtverditPopolnenie(sum))
            {
                BankDialogi.OperaciyaOtmenena();
                return;
            }
            string rez = servis.Popolnit(sum);
            Console.WriteLine(rez);
            if (rez == "Пополнение выполнено")
                BankDialogi.PopolnenieUspeshno(sum, servis.Tekushiy.Balans);
            else if (rez == "Сначала войдите в систему")
                BankDialogi.NetVhoda();
        }

        static void Snyat()
        {
            if (servis.Tekushiy == null)
            {
                BankDialogi.NetVhoda();
                return;
            }
            decimal sum = ChitatSummu();
            if (sum <= 0)
            {
                BankDialogi.SummaNePodhodit();
                return;
            }
            if (!BankDialogi.PodtverditSnyatie(sum))
            {
                BankDialogi.OperaciyaOtmenena();
                return;
            }
            string rez = servis.Snyat(sum);
            Console.WriteLine(rez);
            if (rez == "Снятие выполнено")
                BankDialogi.SnyatieUspeshno(sum, servis.Tekushiy.Balans);
            else if (rez == "Недостаточно средств")
                BankDialogi.NedostatochnoSredstv();
            else if (rez == "Сначала войдите в систему")
                BankDialogi.NetVhoda();
        }

        static void Perevod()
        {
            if (servis.Tekushiy == null)
            {
                BankDialogi.NetVhoda();
                return;
            }
            Console.Write("Логин получателя: ");
            string login = Console.ReadLine();
            decimal sum = ChitatSummu();
            if (sum <= 0)
            {
                BankDialogi.SummaNePodhodit();
                return;
            }
            if (!BankDialogi.PodtverditPerevod(login, sum))
            {
                BankDialogi.OperaciyaOtmenena();
                return;
            }
            string rez = servis.Perevod(login, sum);
            Console.WriteLine(rez);
            if (rez == "Перевод выполнен")
                BankDialogi.PerevodUspeshno(login, sum);
            else if (rez == "Получатель не найден")
                BankDialogi.PoluchatelNeNayden();
            else if (rez == "Нельзя перевести себе")
                BankDialogi.PerevodSebe();
            else if (rez == "Недостаточно средств")
                BankDialogi.NedostatochnoSredstv();
            else if (rez == "Сначала войдите в систему")
                BankDialogi.NetVhoda();
        }

        static void DialogZagruzka()
        {
            string rez = servis.ZagruzitIzDialoga();
            Console.WriteLine(rez);
            if (rez == "Загрузка отменена")
                BankDialogi.OperaciyaOtmenena();
        }

        static void DialogSohranenie()
        {
            string rez = servis.SohranitVDialog();
            Console.WriteLine(rez);
            if (rez == "Сохранение отменено")
                BankDialogi.OperaciyaOtmenena();
        }

        static void Sverka()
        {
            servis.SdelatSverku();
            BankDialogi.SverkaZavershena();
        }
    }
}
