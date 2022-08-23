
namespace bb.Optik_PY
    {
    partial class Form1
        {
        /// <summary>
        ///Gerekli tasarımcı değişkeni.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///Kullanılan tüm kaynakları temizleyin.
        /// </summary>
        ///<param name="disposing">yönetilen kaynaklar dispose edilmeliyse doğru; aksi halde yanlış.</param>
        protected override void Dispose(bool disposing)
            {
            if (disposing && (components != null))
                {
                components.Dispose();
                }
            base.Dispose(disposing);
            }

        #region Windows Form Designer üretilen kod

        /// <summary>
        /// Tasarımcı desteği için gerekli metot - bu metodun 
        ///içeriğini kod düzenleyici ile değiştirmeyin.
        /// </summary>
        private void InitializeComponent()
            {
            this.components = new System.ComponentModel.Container();
            this.label1 = new System.Windows.Forms.Label();
            this.lbCevapKagitlari = new System.Windows.Forms.Label();
            this.btnCevapKagitlari = new System.Windows.Forms.Button();
            this.btnOgrenciKagitlari = new System.Windows.Forms.Button();
            this.lbOgrenciKagitlari = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.btnIsle = new System.Windows.Forms.Button();
            this.progressBar1 = new System.Windows.Forms.ProgressBar();
            this.timer1 = new System.Windows.Forms.Timer(this.components);
            this.txtSonuc = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.lblSonuc = new System.Windows.Forms.Label();
            this.folderBrowserDialog1 = new System.Windows.Forms.FolderBrowserDialog();
            this.folderBrowserDialog2 = new System.Windows.Forms.FolderBrowserDialog();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(15, 32);
            this.label1.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(86, 15);
            this.label1.TabIndex = 0;
            this.label1.Text = "Cevap Kağıtları";
            // 
            // lbCevapKagitlari
            // 
            this.lbCevapKagitlari.Location = new System.Drawing.Point(261, 32);
            this.lbCevapKagitlari.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
            this.lbCevapKagitlari.Name = "lbCevapKagitlari";
            this.lbCevapKagitlari.Size = new System.Drawing.Size(355, 23);
            this.lbCevapKagitlari.TabIndex = 1;
            this.lbCevapKagitlari.Text = "Cevap Anahtarları";
            // 
            // btnCevapKagitlari
            // 
            this.btnCevapKagitlari.Location = new System.Drawing.Point(165, 26);
            this.btnCevapKagitlari.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
            this.btnCevapKagitlari.Name = "btnCevapKagitlari";
            this.btnCevapKagitlari.Size = new System.Drawing.Size(88, 27);
            this.btnCevapKagitlari.TabIndex = 2;
            this.btnCevapKagitlari.Text = "Aç";
            this.btnCevapKagitlari.UseVisualStyleBackColor = true;
            this.btnCevapKagitlari.Click += new System.EventHandler(this.btnCevapKagitlari_Click);
            // 
            // btnOgrenciKagitlari
            // 
            this.btnOgrenciKagitlari.Location = new System.Drawing.Point(165, 72);
            this.btnOgrenciKagitlari.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
            this.btnOgrenciKagitlari.Name = "btnOgrenciKagitlari";
            this.btnOgrenciKagitlari.Size = new System.Drawing.Size(88, 27);
            this.btnOgrenciKagitlari.TabIndex = 5;
            this.btnOgrenciKagitlari.Text = "Aç";
            this.btnOgrenciKagitlari.UseVisualStyleBackColor = true;
            this.btnOgrenciKagitlari.Click += new System.EventHandler(this.btnOgrenciKagitlari_Click);
            // 
            // lbOgrenciKagitlari
            // 
            this.lbOgrenciKagitlari.Location = new System.Drawing.Point(261, 76);
            this.lbOgrenciKagitlari.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
            this.lbOgrenciKagitlari.Name = "lbOgrenciKagitlari";
            this.lbOgrenciKagitlari.Size = new System.Drawing.Size(355, 23);
            this.lbOgrenciKagitlari.TabIndex = 4;
            this.lbOgrenciKagitlari.Text = "Optik Formlar";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(15, 84);
            this.label2.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(95, 15);
            this.label2.TabIndex = 3;
            this.label2.Text = "Öğrenci Kağıtları";
            // 
            // btnIsle
            // 
            this.btnIsle.Location = new System.Drawing.Point(165, 176);
            this.btnIsle.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
            this.btnIsle.Name = "btnIsle";
            this.btnIsle.Size = new System.Drawing.Size(88, 27);
            this.btnIsle.TabIndex = 6;
            this.btnIsle.Text = "İşle";
            this.btnIsle.UseVisualStyleBackColor = true;
            this.btnIsle.Click += new System.EventHandler(this.btnIsle_Click);
            // 
            // progressBar1
            // 
            this.progressBar1.Location = new System.Drawing.Point(13, 224);
            this.progressBar1.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
            this.progressBar1.Name = "progressBar1";
            this.progressBar1.Size = new System.Drawing.Size(603, 27);
            this.progressBar1.TabIndex = 7;
            // 
            // txtSonuc
            // 
            this.txtSonuc.Location = new System.Drawing.Point(165, 128);
            this.txtSonuc.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
            this.txtSonuc.Name = "txtSonuc";
            this.txtSonuc.Size = new System.Drawing.Size(451, 23);
            this.txtSonuc.TabIndex = 9;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(15, 128);
            this.label3.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(142, 15);
            this.label3.TabIndex = 8;
            this.label3.Text = "Sonuc Dosyası Adı (Excel)";
            // 
            // lblSonuc
            // 
            this.lblSonuc.AutoSize = true;
            this.lblSonuc.Location = new System.Drawing.Point(283, 164);
            this.lblSonuc.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.lblSonuc.Name = "lblSonuc";
            this.lblSonuc.Size = new System.Drawing.Size(0, 15);
            this.lblSonuc.TabIndex = 10;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(620, 270);
            this.Controls.Add(this.lblSonuc);
            this.Controls.Add(this.txtSonuc);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.progressBar1);
            this.Controls.Add(this.btnIsle);
            this.Controls.Add(this.btnOgrenciKagitlari);
            this.Controls.Add(this.lbOgrenciKagitlari);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.btnCevapKagitlari);
            this.Controls.Add(this.lbCevapKagitlari);
            this.Controls.Add(this.label1);
            this.Margin = new System.Windows.Forms.Padding(1);
            this.Name = "Form1";
            this.Text = "Form1";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

            }

        #endregion
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label lbCevapKagitlari;
        private System.Windows.Forms.Button btnCevapKagitlari;
        private System.Windows.Forms.Button btnOgrenciKagitlari;
        private System.Windows.Forms.Label lbOgrenciKagitlari;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Button btnIsle;
        private System.Windows.Forms.ProgressBar progressBar1;
        private System.Windows.Forms.Timer timer1;
        private System.Windows.Forms.TextBox txtSonuc;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label lblSonuc;
        private System.Windows.Forms.FolderBrowserDialog folderBrowserDialog1;
        private System.Windows.Forms.FolderBrowserDialog folderBrowserDialog2;
        }
    }

