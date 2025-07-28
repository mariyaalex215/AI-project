import java.util.Scanner;

class q23{
    public static void main(String args[]){
        //for 1 to 5
        // for(int i=1;i<=5;i=i+1)
        // {
        //     System.out.print(i);
        // }
            Scanner scan = new Scanner(System.in);
            System.out.print("Number 1");
            int a = scan.nextInt();
            System.out.print("Number 2");
            int b = scan.nextInt();

            for(int i=a;i<=b;i=i+1)
            {
                System.out.println(i);

            }



    }
}