import java.util.Scanner;

class q12{
    public static void main(String args[])
    {
        Scanner scan = new Scanner(System.in);
        int income = scan.nextInt();

        if(income>7000)
        {
            System.out.print("Scholarship is available");
        }
        else{

            System.out.print("Not eligible for scholarship");
            
        }

    }
}