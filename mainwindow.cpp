#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QRect>
#include <QDesktopWidget>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    QRect position = frameGeometry();
    position.moveCenter(QDesktopWidget().availableGeometry().center());
    move(position.topLeft());

    QList<QPrinterInfo> pinfo;
    pinfo = PrinterInfo.availablePrinters();
    foreach(QPrinterInfo p0, pinfo) {
        ui->comboBox->addItem( p0.printerName() );
    }
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_pushButton_clicked()
{
    print_ticket( ui->comboBox->currentText() );
}

void MainWindow::print_ticket(QString pname)
{
    QList<QPrinterInfo> pinfo;
    pinfo = PrinterInfo.availablePrinters();
    int jobId = 0;

    foreach(QPrinterInfo p0, pinfo) {
        if( p0.printerName() == pname )
        {
            jobId = cupsCreateJob( CUPS_HTTP_DEFAULT, pname.toStdString().c_str(), "ticket", 0, NULL );

            if ( jobId > 0 )
            {
                const char* format = CUPS_FORMAT_TEXT;  // CUPS_FORMAT_POSTSCRIPT;
                char* text = new char[15];
                strcpy(text, "Hola mundo!\n");
                cupsStartDocument( CUPS_HTTP_DEFAULT, pname.toStdString().c_str(), jobId, text, format, true );
                cupsWriteRequestData( CUPS_HTTP_DEFAULT, text, strlen(text) );
                cupsFinishDocument( CUPS_HTTP_DEFAULT, pname.toStdString().c_str() );
            }
        }
    }
}
