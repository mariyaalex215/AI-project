import java.util.Scanner;

class q20{
    public static void main(String args[])
    {
        Scanner scan = new Scanner(System.in);

        System.out.print("Enter your salary:");
        int salary = scan.nextInt();
        System.out.print("What is your Age:");
        int Age = scan.nextInt();

        if(salary>20000 || Age<25)
        {
            System.out.println("Eligible for Loan");
            System.out.print("How much loan do you need?");
            int loan = scan.nextInt();

        if(loan<50000)
        {
            System.out.print("Loan Available");

        }

        }
    }
}