import java.util.*;
import java.io.*;
/**
 * Write a description of class Individual here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class Individual
{
    // instance variables - replace the example below with your own
    private double[] genes = new double[6];
    private double fitnessValue;
    
   
    

    /**
     * Constructor for objects of class Individual
     */
    public Individual(double[] datX, double[] datY)
    {
        // initialise instance variables
     
        baseGenes();
        calcFitness(datX, datY);
      // System.out.println(getGene(0)+ ": " + getGene(1)+ ": " + getGene(2)+ ": " + getGene(3)+ ": " + getGene(4)+ ": " + getGene(5));
      //  mutate();
      //  System.out.println(getGene(0)+ ": " + getGene(1)+ ": " + getGene(2)+ ": " + getGene(3)+ ": " + getGene(4)+ ": " + getGene(5));
      //   for(int i=0;i<genes.length;i++)
      //   {
      //       System.out.println(getGene(i));
      //   }   
    }
   
    public void baseGenes()
    {
        //First round
        double rand = new Random().nextDouble();
        //A can be inferred from the graph 
        double randomGene = (rand * 1) + -1;
        setGene(0,randomGene);
        //Seecond Round
        rand = new Random().nextDouble();
        randomGene = (rand * 2000) + -1000;
        setGene(1, randomGene);
        //Third roudn
        rand = new Random().nextDouble();
        randomGene = (rand * 2000) + -1000;
        setGene(2, randomGene);
        //Fourth Round
        rand = new Random().nextDouble();
        randomGene = (rand * 200) + -100;
        setGene(3, randomGene);
        //Fifth Round
        rand = new Random().nextDouble();
        randomGene = (rand * 20) + -10;
        setGene(4, randomGene);
        //Sixth Round
        rand = new Random().nextDouble();
        randomGene = (rand * 2) + -1;
        setGene(5, randomGene);
    }
    
    public double getFitnessValue()
    {
        return fitnessValue;
    }
    
    public void setFitnessValue(double fitnessValue)
    {
        this.fitnessValue = fitnessValue;
    }
    
    public double getGene(int index)
    {
        return genes[index];
    }
    
    public void setGene(int index, double gene)
    {
        this.genes[index] = gene;
    }
    
    /**
     * Mutate needs to select a gene at random
     * depending on gene index (case) mutate to power^10
     * 0 = 0.00001 -> 10,000
     * 1 = 0.00001 -> 1,000
     * 2 = 0.00001 -> 100
     * 3 = 0.00001 -> 10
     * 4 = 0.00001 -> 1
     * 5 = 0.00001 -> 0.1
     */
    public void rapidMutate(Integer factor)
    {
        double rnd = new Random().nextDouble();
        int rndAddorSub = new Random().nextInt(1 + 1);
        double newGene;
        Random randD = new Random();
        double mutationSize = 0;;
        if(factor == null){factor = 1;}
        for(int i=0;i<6;i++)
        {
            if(i == 0){mutationSize = 0.1;}
            if(i == 1){mutationSize = 1000;}
            if(i == 2){mutationSize = 100;}
            if(i == 3){mutationSize = 100;}
            if(i == 4){mutationSize = 10;}
            if(i == 5){mutationSize = 1;}
            
            rnd = new Random().nextDouble();
            if(rnd > 0.5)
            {
                newGene = factor*(randD.nextDouble()*mutationSize);
                if(rndAddorSub == 0){
                    //System.out.println("TO BE ADDED : " + newGene);
                        newGene = getGene(i)- newGene;
                    //System.out.println("NG : " + newGene + " Minused");
                }
                if(rndAddorSub == 1){
                        newGene = getGene(i) + newGene;
                    //System.out.println("NG : " + newGene + " added");
                }
               // System.out.println("PREV GENE : "+ getGene(i));
                setGene(i, newGene);
                //System.out.println("NEW GENE : "+ getGene(i));
            }
        }
        
        
    }
    
     public void mutate(Integer factor)
    {
        int rnd = new Random().nextInt(5 + 1);
        int rndAddorSub = new Random().nextInt(1 + 1);
        double newGene;
        Random randD = new Random();
        if(factor == null){factor = 1;}
        switch(rnd){
            case 0: newGene = factor*(randD.nextDouble()*0.1);
                    if(rndAddorSub == 0){
                        newGene = getGene(0)- newGene;}
                    if(rndAddorSub == 1){
                        newGene = getGene(0) + newGene;}
                    setGene(0, newGene);
                    break;
            case 1: newGene = factor*(randD.nextDouble()*100);
                    if(rndAddorSub == 0){
                        newGene = getGene(1)- newGene;}
                    if(rndAddorSub == 1){
                        newGene = getGene(1) + newGene;}
                    setGene(1, newGene);
                    break;
            case 2: newGene = factor*(randD.nextDouble()*100);
                    if(rndAddorSub == 0){
                        newGene = getGene(2)- newGene;}
                    if(rndAddorSub == 1){
                        newGene = getGene(2) + newGene;}
                    setGene(2, newGene);
                    break;
            case 3: newGene = factor*(randD.nextDouble()*10);
                    if(rndAddorSub == 0){
                        newGene = getGene(3)- newGene;}
                    if(rndAddorSub == 1){
                        newGene = getGene(3) + newGene;}
                    setGene(3, newGene);
                    break;
            case 4: newGene = factor*(randD.nextDouble()*1);
                    if(rndAddorSub == 0){
                        newGene = getGene(4)- newGene;}
                    if(rndAddorSub == 1){
                        newGene = getGene(4) + newGene;}
                    setGene(4, newGene);
                    break;
            case 5: newGene = factor*(randD.nextDouble()*0.01);
                    if(rndAddorSub == 0){
                        newGene = getGene(5)- newGene;}
                    if(rndAddorSub == 1){
                        newGene = getGene(5) + newGene;}
                    setGene(5, newGene);
                    break;
            default: System.out.println("MUTATION PROBLEM");
                    break;
                    
                    
                    
        }
        
    }
    
    public static double evalpoly(double[] c, double x)
    {
        int n = c.length - 1;
        double y = c[n];
        for (int i = n - 1; i >= 0; i--) {
            y = c[i] + (x * y);
        }
        return y;
    } 
    
    
    public void calcFitness(double[] datX, double[] datY)
    {
        //for each X, do poly, add result to total, average 
        
        double[] genes = this.genes;
        double fitnessResult = 0.0;
        double newResult = 0.0;
        for(int i=0;i<datX.length;i++){
          newResult = evalpoly(genes, datX[i]);
          newResult = newResult - datY[i];
          newResult = Math.pow(newResult,2);
          newResult = Math.sqrt(newResult);
          fitnessResult += newResult;
        }
        fitnessResult = fitnessResult/577;
        setFitnessValue(fitnessResult);
    }
    
  

}
