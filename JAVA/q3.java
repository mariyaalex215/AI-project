import java.util.Scanner;

class q3{
    public static void main(String args[])
    {
        Scanner scan = new Scanner(System.in);
        String name = scan.nextLine();
        double score = scan.nextInt();
        scan.nextLine();
        String department = scan.nextLine();

        System.out.println("My name is "+name);
        System.out.println("My score is "+score/10 +"/10");
        System.out.print("my department is "+department);

    }

}