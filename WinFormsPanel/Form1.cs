using System.Drawing;
using System.Windows.Forms;

namespace WinFormsPanel
{
    public class Form1 : Form
    {
        public Form1()
        {
            Text = "Панели и вкладки";
            Size = new Size(500, 400);
            StartPosition = FormStartPosition.CenterScreen;

            TabControl vkladki = new TabControl();
            vkladki.Dock = DockStyle.Fill;

            TabPage stranica1 = new TabPage("Главная");
            GroupBox gruppa1 = new GroupBox();
            gruppa1.Text = "Данные клиента";
            gruppa1.Location = new Point(15, 15);
            gruppa1.Size = new Size(420, 120);

            Label lblFio = new Label();
            lblFio.Text = "ФИО:";
            lblFio.Location = new Point(15, 30);
            lblFio.AutoSize = true;

            TextBox poleFio = new TextBox();
            poleFio.Location = new Point(80, 27);
            poleFio.Width = 300;
            poleFio.Text = "Мамедова Мадина Айдынгызы";

            Label lblBalans = new Label();
            lblBalans.Text = "Баланс:";
            lblBalans.Location = new Point(15, 65);
            lblBalans.AutoSize = true;

            TextBox poleBalans = new TextBox();
            poleBalans.Location = new Point(80, 62);
            poleBalans.Width = 150;
            poleBalans.Text = "5000";

            gruppa1.Controls.Add(lblFio);
            gruppa1.Controls.Add(poleFio);
            gruppa1.Controls.Add(lblBalans);
            gruppa1.Controls.Add(poleBalans);

            Panel panel1 = new Panel();
            panel1.Location = new Point(15, 150);
            panel1.Size = new Size(420, 150);
            panel1.BorderStyle = BorderStyle.FixedSingle;
            panel1.BackColor = Color.WhiteSmoke;

            Label tekstPanel = new Label();
            tekstPanel.Text = "Это панель Panel";
            tekstPanel.Location = new Point(20, 20);
            tekstPanel.AutoSize = true;

            Button knopka = new Button();
            knopka.Text = "Нажми";
            knopka.Location = new Point(20, 60);
            knopka.Click += (s, e) =>
            {
                MessageBox.Show("Привет, " + poleFio.Text);
            };

            panel1.Controls.Add(tekstPanel);
            panel1.Controls.Add(knopka);

            stranica1.Controls.Add(gruppa1);
            stranica1.Controls.Add(panel1);

            TabPage stranica2 = new TabPage("Операции");
            GroupBox gruppa2 = new GroupBox();
            gruppa2.Text = "Перевод";
            gruppa2.Location = new Point(15, 15);
            gruppa2.Size = new Size(420, 100);

            Label lblKomu = new Label();
            lblKomu.Text = "Кому:";
            lblKomu.Location = new Point(15, 35);
            lblKomu.AutoSize = true;

            TextBox poleKomu = new TextBox();
            poleKomu.Location = new Point(80, 32);
            poleKomu.Width = 200;

            Label lblSumma = new Label();
            lblSumma.Text = "Сумма:";
            lblSumma.Location = new Point(15, 65);
            lblSumma.AutoSize = true;

            TextBox poleSumma = new TextBox();
            poleSumma.Location = new Point(80, 62);
            poleSumma.Width = 100;

            gruppa2.Controls.Add(lblKomu);
            gruppa2.Controls.Add(poleKomu);
            gruppa2.Controls.Add(lblSumma);
            gruppa2.Controls.Add(poleSumma);

            Panel panel2 = new Panel();
            panel2.Dock = DockStyle.Bottom;
            panel2.Height = 50;
            panel2.BackColor = Color.LightSteelBlue;

            Button knopkaPerevod = new Button();
            knopkaPerevod.Text = "Перевести";
            knopkaPerevod.Location = new Point(15, 10);
            knopkaPerevod.Click += (s, e) =>
            {
                MessageBox.Show("Перевод " + poleSumma.Text + " руб.");
            };

            panel2.Controls.Add(knopkaPerevod);

            stranica2.Controls.Add(gruppa2);
            stranica2.Controls.Add(panel2);

            vkladki.TabPages.Add(stranica1);
            vkladki.TabPages.Add(stranica2);

            Controls.Add(vkladki);
        }
    }
}
