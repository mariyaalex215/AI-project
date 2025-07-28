import java.util.Scanner;

class q18{
    public static void main(String args[])
    {
        Scanner scan = new Scanner(System.in);
        int sub1 = scan.nextInt();
        int sub2 = scan.nextInt();
        int sub3 = scan.nextInt();
        int sub4 = scan.nextInt();
        int sub5 = scan.nextInt();

        int Totalmark = sub1+sub2+sub3+sub4+sub5;

        int Average = Totalmark/5;

        if(Average<35)
        {
            System.out.print("Additional class required");
        }
        else{
            System.out.print("Very Good");
            
        }

    }
}