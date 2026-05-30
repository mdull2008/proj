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

    class BankDialogi
    {
        static void Pokazat(string text, string zagolovok, MessageBoxIcon ikonka)
        {
            MessageBox.Show(text, zagolovok, MessageBoxButtons.OK, ikonka);
        }

        static bool Sprosit(string text, string zagolovok, MessageBoxIcon ikonka)
        {
            DialogResult otvet = MessageBox.Show(
                text,
                zagolovok,
                MessageBoxButtons.YesNo,
                ikonka
            );
            return otvet == DialogResult.Yes;
        }

        public static void Privetstvie()
        {
            Pokazat(
                "Консольный банк готов к работе.\nВыберите действие в меню.",
                "Добро пожаловать",
                MessageBoxIcon.Information
            );
        }

        public static void NetPunktaMenu()
        {
            Pokazat(
                "Такого номера нет в меню.\nВведите число от 0 до 9.",
                "Ошибка меню",
                MessageBoxIcon.Error
            );
        }

        public static void NetVhoda()
        {
            Pokazat(
                "Сначала войдите в систему (пункт 2).",
                "Требуется вход",
                MessageBoxIcon.Warning
            );
        }

        public static void NevernayaSumma()
        {
            Pokazat(
                "Сумма должна быть числом больше нуля.",
                "Ошибка ввода",
                MessageBoxIcon.Error
            );
        }

        public static void LoginZanyat()
        {
            Pokazat(
                "Этот логин уже есть или поле пустое.\nПридумайте другой логин.",
                "Регистрация невозможна",
                MessageBoxIcon.Warning
            );
        }

        public static void SchetSozdan(string login)
        {
            Pokazat(
                "Счет \"" + login + "\" открыт.\nБаланс: 0 руб.",
                "Регистрация успешна",
                MessageBoxIcon.Information
            );
        }

        public static void VhodUspeshno(string login)
        {
            Pokazat(
                "Вы вошли как " + login + ".\nМожно работать со счетом.",
                "Вход выполнен",
                MessageBoxIcon.Information
            );
        }

        public static void KlientNeNayden()
        {
            Pokazat(
                "Пользователь с таким логином не найден.",
                "Ошибка входа",
                MessageBoxIcon.Error
            );
        }

        public static void NeverniyParol()
        {
            Pokazat(
                "Пароль не подходит.\nПопробуйте еще раз.",
                "Ошибка входа",
                MessageBoxIcon.Error
            );
        }

        public static void PokazatBalans(decimal balans)
        {
            Pokazat(
                "На вашем счете:\n" + balans + " руб.",
                "Баланс счета",
                MessageBoxIcon.Information
            );
        }

        public static bool PodtverditPopolnenie(decimal summa)
        {
            return Sprosit(
                "Зачислить на счет " + summa + " руб.?",
                "Подтверждение пополнения",
                MessageBoxIcon.Question
            );
        }

        public static bool PodtverditSnyatie(decimal summa)
        {
            return Sprosit(
                "Выдать наличными " + summa + " руб.?",
                "Подтверждение снятия",
                MessageBoxIcon.Question
            );
        }

        public static bool PodtverditPerevod(string komu, decimal summa)
        {
            return Sprosit(
                "Перевести " + summa + " руб.\nполучателю " + komu + "?",
                "Подтверждение перевода",
                MessageBoxIcon.Question
            );
        }

        public static void PopolnenieUspeshno(decimal summa, decimal balans)
        {
            Pokazat(
                "Зачислено " + summa + " руб.\nНовый баланс: " + balans + " руб.",
                "Пополнение выполнено",
                MessageBoxIcon.Information
            );
        }

        public static void SnyatieUspeshno(decimal summa, decimal balans)
        {
            Pokazat(
                "Снято " + summa + " руб.\nОстаток: " + balans + " руб.",
                "Снятие выполнено",
                MessageBoxIcon.Information
            );
        }

        public static void PerevodUspeshno(string komu, decimal summa)
        {
            Pokazat(
                "Перевод " + summa + " руб.\nотправлен клиенту " + komu + ".",
                "Перевод выполнен",
                MessageBoxIcon.Information
            );
        }

        public static void NedostatochnoSredstv()
        {
            Pokazat(
                "На счете не хватает денег для этой операции.",
                "Операция отклонена",
                MessageBoxIcon.Warning
            );
        }

        public static void PerevodSebe()
        {
            Pokazat(
                "Нельзя переводить деньги на свой же счет.",
                "Перевод невозможен",
                MessageBoxIcon.Warning
            );
        }

        public static void PoluchatelNeNayden()
        {
            Pokazat(
                "Клиент с таким логином не найден.",
                "Перевод невозможен",
                MessageBoxIcon.Error
            );
        }

        public static void SummaNePodhodit()
        {
            Pokazat(
                "Сумма должна быть больше нуля.",
                "Ошибка суммы",
                MessageBoxIcon.Warning
            );
        }

        public static void FaylZagruzhen(string put)
        {
            Pokazat(
                "База клиентов загружена из файла:\n" + put,
                "Файл открыт",
                MessageBoxIcon.Information
            );
        }

        public static void FaylSohranen(string put)
        {
            Pokazat(
                "Данные записаны в файл:\n" + put,
                "Файл сохранен",
                MessageBoxIcon.Information
            );
        }

        public static void OperaciyaOtmenena()
        {
            Pokazat(
                "Действие отменено пользователем.",
                "Отмена",
                MessageBoxIcon.Warning
            );
        }

        public static void SverkaZavershena()
        {
            Pokazat(
                "Сверка памяти и bank.txt выполнена.\nПодробности в консоли.",
                "Сверка данных",
                MessageBoxIcon.Information
            );
        }

        public static bool VyhodSohranit()
        {
            return Sprosit(
                "Сохранить базу в bank.txt и выйти?",
                "Выход из программы",
                MessageBoxIcon.Question
            );
        }

        public static bool VyhodBezSohraneniya()
        {
            return Sprosit(
                "Выйти без сохранения изменений?",
                "Внимание",
                MessageBoxIcon.Warning
            );
        }

        public static void DoSvidaniya()
        {
            Pokazat(
                "Спасибо, что пользовались банком.",
                "До свидания",
                MessageBoxIcon.Information
            );
        }

        public static void VyhodOtmenen()
        {
            Pokazat(
                "Вы остались в программе.",
                "Выход отменен",
                MessageBoxIcon.Information
            );
        }
    }

    class BankFaylDialog
    {
        public bool ZagruzitCherezDialog(SpisokKlientov<Klient> baza)
        {
            OpenFileDialog otkrit = new OpenFileDialog();
            otkrit.Filter = "Файл банка (*.txt)|*.txt|Все файлы (*.*)|*.*";
            otkrit.Title = "Открыть базу клиентов";
            otkrit.InitialDirectory = Environment.CurrentDirectory;
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
            BankDialogi.FaylZagruzhen(otkrit.FileName);
            return true;
        }

        public bool SohranitCherezDialog(SpisokKlientov<Klient> baza)
        {
            SaveFileDialog sohranit = new SaveFileDialog();
            sohranit.Filter = "Файл банка (*.txt)|*.txt|Все файлы (*.*)|*.*";
            sohranit.Title = "Сохранить базу клиентов";
            sohranit.FileName = "bank.txt";
            sohranit.InitialDirectory = Environment.CurrentDirectory;
            if (sohranit.ShowDialog() != DialogResult.OK)
                return false;
            List<string> stroki = new List<string>();
            foreach (Klient k in baza.Vse())
            {
                stroki.Add(k.Login + ";" + k.Parol + ";" + k.Balans);
            }
            File.WriteAllLines(sohranit.FileName, stroki);
            BankDialogi.FaylSohranen(sohranit.FileName);
            return true;
        }
    }
}
