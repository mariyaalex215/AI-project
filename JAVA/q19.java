import java.util.Scanner;

class q19{
    public static void main(String args[])
    {
        Scanner scan = new Scanner(System.in);
        int salary = scan.nextInt();
        int Age = scan.nextInt();

        if(salary>=7000 || Age<25)
        {
           
            System.out.print( " Eligible for loan ");

        }
        else
        {
            
            System.out.print( " No loan ");
       
        }
    }
}


