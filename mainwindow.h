#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QList>
#include <QPrinter>
#include <QPrinterInfo>
#include <QString>
#include <cups/cups.h>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT
    
public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private slots:
    void on_pushButton_clicked();

private:
    Ui::MainWindow *ui;
    QPrinterInfo PrinterInfo;
    void print_ticket(QString pname);
};

#endif // MAINWINDOW_H
