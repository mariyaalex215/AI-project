import java.util.Scanner;
class q6{
    public static void main(String args[])
    {
        //Check whether Number 1 and Number 2 is Equal or not

        Scanner scan = new Scanner(System.in);
        int num1 = scan.nextInt();
        int num2 = scan.nextInt();

        if (num1==num2)
        {
            System.out.print("Both the Numbers are Equal");

        }
        else{
            System.out.print("Not Equal");

        }
    }
}