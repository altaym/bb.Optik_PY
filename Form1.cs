using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using IronPython.Hosting;


namespace bb.Optik_PY
    {
    public partial class Form1 : Form
        {
        public Form1()
            {
            InitializeComponent();
            }

        public string baseDirectory;
        public string bbPythonApp;

        public string FolderAnswerKeys;
        public string FolderOptikForms;
        public string OutputFile;

        private void Form1_Load(object sender, EventArgs e)
            {
            //baseDirectory = "D://_temp//optik//";
            //bbPythonApp = "D://_temp//optik//main.py";

            baseDirectory = Environment.CurrentDirectory;
            bbPythonApp = Path.Combine(Environment.CurrentDirectory, "main.py");
            }


        private void btnCevapKagitlari_Click(object sender, EventArgs e)
            {
            if (folderBrowserDialog1.ShowDialog() == DialogResult.OK)
                {
                lbCevapKagitlari.Text = FolderAnswerKeys = folderBrowserDialog1.SelectedPath;
                }
            else
                {
                lblSonuc.Text += "Cevap Anahtarlarının bulunduğu klasörü seçiniz.";
                return;
                }



            }
        private void OptikOku(string ogrenciOptik, string cevapAnahtari, string sonucDosyaAdi)
            {
            timer1.Enabled = true;
            progressBar1.Value += 10;


            //string cmdArguments = "/c \"python " + myPythonApp + " " + "--ogrencioptik " + ogrenciOptik + " " + "--cevapkagidi " + cevapAnahtari + " " + "--sonuckayit " + sonucDosyaAdi + "\"";
            string cmdArguments = string.Format("/c \"python {0} --ogrencioptik {1} --cevapkagidi {2} --sonuckayit {3} --sonucisim {4}\"", bbPythonApp, ogrenciOptik, cevapAnahtari, baseDirectory, sonucDosyaAdi);
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = "cmd.exe";
            start.UseShellExecute = false;
            start.WorkingDirectory = baseDirectory;
            start.Arguments = cmdArguments;
            start.RedirectStandardOutput = false;
            start.RedirectStandardError = true;
            start.CreateNoWindow = true;
            Process process = Process.Start(start);
            timer1.Start();
            process.WaitForExit();
            timer1.Stop();
            timer1.Enabled = false;
            progressBar1.Value = 100;
            lblSonuc.Text = "İşlem tamamlandı";
            //MessageBox.Show("İşlem Bitti");
            //button3.Enabled = true;
            }

        private void btnIsle_Click(object sender, EventArgs e)
            {
            //var p1 = Python.CreateEngine();
            //try
            //    {
            //    p1.ExecuteFile("main.py");

            //    }
            //catch (Exception ex)
            //    {

            //    throw ex;
            //    }
            //OptikOku(txtOgrenciKagitlari.Text, txtCevapKagitlari.Text, txtSonuc.Text);
            //OptikOku("ogrenciler", "cevapkagidi", "sonuclar");
            if (!string.IsNullOrEmpty(txtSonuc.Text))
                {
                OutputFile = txtSonuc.Text.Trim();
                }
            else
                {
                lblSonuc.Text += "Sonuç dosya adını yazınız.";
                return;
                }


            if (!string.IsNullOrEmpty(FolderOptikForms) && !string.IsNullOrEmpty(FolderAnswerKeys) && !string.IsNullOrEmpty(OutputFile))
                {
                lblSonuc.Text = "İşlem Başladı";
                OptikOku(FolderOptikForms, FolderAnswerKeys, OutputFile);
                }
            else
                {
                lblSonuc.Text = "Cevap Anahtarı/Optik Form ların bulunduğu klasörü seçiniz.";
                }
            }

        private void btnOgrenciKagitlari_Click(object sender, EventArgs e)
            {
            if (folderBrowserDialog2.ShowDialog() == DialogResult.OK)
                {
                lbOgrenciKagitlari.Text = FolderOptikForms = folderBrowserDialog2.SelectedPath;
                }
            else
                {
                lblSonuc.Text += "Öğrenci optik formlarının olduğu klasörü seçiniz.";
                return;
                }
            }
        }
    }
