import java.util.*;
import java.io.*;
/**
 * Write a description of class Population here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
//Best so far with original mutations - elite = 10, pop = 1990, mut rate 0.2
//359357.20816058316 : 838996.4206373827 : 50372.12722461398 :
// -598.9667697684505 : 2.1649787270774095 : -0.0017144813493944837
//Test against New mutation (each var 50% change to mut, 0.5 chance overall + larger pop

//This problem has LOTS of permutations. Could be more than 1 correct answer?
//Therefore increasing population vs increasing mutation seems critical
//Not sure what gains we get from different selection process. 

//Need to constantly increase diversity while maintaining elite solutions
//and focus
/**
 * TO DO  - FACTOR MUTATION
 * ALSO CHECK FITNESS AFTER MUTATION AND ONLY KEEP IF FITNESS 
 * INCREASES??
 * MAKE COPY OF ELITES AND MUTATE THEM (KEEP IF BETTER?)
 * Possibly limit Crossover to 70% (Cancelled out by need for high diversity)
 * NEW parameter - Generation Gap
 * Add timestamp to start and end of algo
 * 
 * NOTES ORDER OF MUTATION/ELITES/CROSSOVER IMPORTANT TO NOT DESTROY ELITES
 */
public class Population
{
    // instance variables - replace the example below with your own
    static Individual[] myPop;
    static Random rand = new Random(); 
    static private Comparator<Individual> fitnessComparer;
    
    //elite numbers need to be even for now
    final static int Elitism = 10;
    final static int popSize = 990 + Elitism;
    final static int MAX_ITER = 20000;
    final static double MUTATION_RATE = 0.2;
    final static Individual[] elitePop = new Individual[Elitism];
    final static double genGapThreshold = 0.005;
    static double[] datX = datX();
    static double[] datY = datY();   
    
    //At first crossover everyone and see what the results are like
    //final static double CROSSOVER_RATE = 0.7;
    
    
    
    
     static {fitnessComparer = new Comparator<Individual>()
     {
            @Override
            public int compare(Individual ind1, Individual ind2){
                // Java 7 has an Integer#compare function
                return Double.compare(ind1.getFitnessValue(), ind2.getFitnessValue());
            }
     };
    }
    
    public static void main(String[] args)
    {
        Population pop = new Population();
        Individual[] newPop = new Individual[popSize];
        Individual[] indiv = new Individual[2];
        Individual[] elites = new Individual[Elitism];
        double[] genGap = new double[10];
        int genCount = 1;
        int genGapCount = 0;
        double genAverage = 1;
        Integer mutation_factor = 1;
        
        for(int j=0;j<MAX_ITER;j++){
        pop.sortFittest();
        Individual best = pop.popFittest();
        if(genCount%10 == 0){
        System.out.println("GENERATION " + genCount);
        System.out.println(best.getGene(0) +" : "+ best.getGene(1) +" : "+ best.getGene(2) +" : "+ best.getGene(3) +" : "+ best.getGene(4) +" : "+ best.getGene(5) );
        System.out.println("Fittest = " + best.getFitnessValue()); 
        }
        //put 10 fittest into genGap array
        pop.elitePop();
        /**
         * Generation gap calculations for mutation decisions
         * put back in after doing Mutation on elites
         */
        if(genGapCount == 10){
             genAverage = generationGap(genGap);
             genGapCount = 0;
             System.out.println("GENAVG = " + genAverage);
            if(genAverage <= genGapThreshold){
            mutation_factor = 10;
            System.out.println("GEN X FACTORED");
           }
         };
         genGap[genGapCount] = best.getFitnessValue();
         genGapCount++;
        
       
        
        //GEt Ride of Elites[] and just use ElitePop
        int count = 0;
        /**
         * Put elites into the new population
         */
        for(int i=0;i<elites.length;i++)
        {
         newPop[i] = elitePop[i];
         count++;
         //newPop[i+elites.length] = elitePop[i];
         //count++;;
         
         //System.out.println(newPop[i]);
        }
        
       /**
        * copy elites again for later mutation
        */
         for(int i=0;i<elites.length;i++)
        {
         
         newPop[i+elites.length] = elitePop[i];
         count++;;
         
         //System.out.println(newPop[i]);
        }
        //System.out.println("Count : " + count);
         /**
         * Copy elites and mutate them 
         */
        //for(int i=0;i<elites.length;i++){
          //  newPop[count] = elitePop[i];
            //newPop[count].rapidMutate(mutation_factor);
            //newPop[count].calcFitness(datX, datY);
            //count++;
        //}
        //System.out.println("Count : " + count);
        /**
         * Take elites and crossover with random selection of pop
         */
        
        //elites should only cross over with themself?
        for(int i=0;i<elites.length;i++)
        {
            int rnd = new Random().nextInt(pop.popLength());
            indiv = crossover(elitePop[i],pop.getIndiv(rnd));
            newPop[count] = indiv[0];
            newPop[count].calcFitness(datX, datY);
            count++;
            newPop[count] = indiv[1];
            newPop[count].calcFitness(datX, datY);
            count++;
        }
        //System.out.println("Count : " + count);
       /**
        * crossover elites to make elite children
        */
        for(int i=0;i<elites.length;i++)
        {
            indiv = crossover(elitePop[i], elitePop[(i+1)%elites.length]);
            newPop[count] = indiv[0];
            newPop[count].calcFitness(datX, datY);
            count++;
            newPop[count] = indiv[1];
            newPop[count].calcFitness(datX, datY);
            count++;
        }
        /**
         * Cross over the rest of the population randomly 
         * Tournament Selection is introduced as a Side effect of sorting
         * because the sorted list has the best from top to bottom
         * therefore anyone chosen randomly will end up in the same order. 
         */
        //ELITISM*4 - 1 for elitism, 2 for elite children, 1 for mutated elites
        int restOfPop = (popSize-(Elitism*6))/2;
        for(int i=0;i<restOfPop;i++)
        {
            int rnd = new Random().nextInt(pop.popLength());
            int rnd2 = new Random().nextInt(pop.popLength());
            indiv = crossover(pop.getIndiv(rnd), pop.getIndiv(rnd2));
            newPop[count] = indiv[0];
            newPop[count].calcFitness(datX, datY);
            count++;
            newPop[count] = indiv[1];
            newPop[count].calcFitness(datX, datY);
            count++;
        }
        //System.out.println("FINAL Count : " + count);
        /**
         * Mutate elites only first
         */
        int check = 0; //Mutation check count
        for(int i = Elitism;i<Elitism*2;i++)
        {
            //System.out.println("I IS NOW = " + i);
            newPop[i].mutate(mutation_factor);
            newPop[i].calcFitness(datX, datY);
            check++;
        }
       
        /**
         * go through population from ElITISM onwards 
         * Rand.nextDouble <= mutation rate 
         * Mutate
         * 
         */
        //*2 eliitism removed to
        for(int i=(Elitism*2);i<popSize;i++)
        {
            double rndMut = rand.nextDouble();
            if(rndMut <= MUTATION_RATE)
            {
                newPop[i].mutate(mutation_factor);
                newPop[i].calcFitness(datX, datY);
                check++;
            }
            
        }
        
        if(genCount%10 == 0){
            System.out.println("MUTATED " + check);
        }
        /**
         * Move new population into myPop
         */
        setPopulation(newPop);
        //Copy newpop into my pop
        //Calc new fitness for everyone 
        genCount++;
       }

    }
    
    /**
     * Determines if the population has diversivied enough since 
     * previous iterations
     */
    public static double generationGap(double[] genGap)
    {
      double genGapResults = 0;
      for(int i=0;i<genGap.length-1;i++)
      {
          genGapResults += 100-((genGap[i+1]/genGap[i])*100);
      }
      genGapResults = genGapResults/10;
      return genGapResults;
    }
    
    /**
     * Constructor for objects of class Population
     */
    private Population()
    {
        myPop = new Individual[popSize];
        //Initialise POP
        for(int i=0;i<myPop.length;i++)
        {
            myPop[i] = new Individual(datX, datY);
        }
        
        // System.out.println(myPop[0].getGene(0));
    }

    /**
     * sorts myPop and puts the fittest at the top
     */
    private void sortFittest()
    {
        Arrays.sort(myPop, fitnessComparer); 
    }
    
    /**
     * copies Elite amount of entries from myPop (current) to elite 
     * array, ready for new pop.
     * Only do after myPop has been sorted
     */
    private void elitePop()
    {
        System.arraycopy(myPop, 0, elitePop, 0, Elitism);
        //return Arrays.copyOfRange(myPop, myPop.length-500, myPop.length);
    }
    
    /**
     * Get the fittest from the current Generation - only do after
     * array has been sorted
     **/
    private Individual popFittest()
    {
        return myPop[0];
    }
    
    /**
     * Copies the entire new population back into myPop
     **/
    private static void setPopulation(Individual[] newPop)
    {
        System.arraycopy(newPop, 0, myPop, 0, popSize);
    }
    
    /**
     * returns current population
     */
    private Individual[] getPop()
    {
        return this.myPop;
    }
    
    public int popLength()
    {
        return myPop.length;
    }
    
    /**
     * Return individual from population
     */
    private Individual getIndiv(int index)
    {
        return myPop[index];
    }
    //CROSSOVER METHOD
    /**
     * Crossover method
     */
    private static Individual[] crossover(Individual ind1, Individual ind2)
    {
        Individual[] newIndiv = new Individual[2];
        newIndiv[0] = new Individual(datX, datY);
        newIndiv[1] = new Individual(datX, datY);
       // System.out.println("BEFORE");
       // System.out.println("FIRST");
        //System.out.println(ind1.getGene(0) + " " + ind1.getGene(1) + " " + ind1.getGene(2) + " " + ind1.getGene(3) + " " + ind1.getGene(4) + " " + ind1.getGene(5));
       // System.out.println("SECOND");
       // System.out.println(ind2.getGene(0) + " " + ind2.getGene(1) + " " + ind2.getGene(2) + " " + ind2.getGene(3) + " " + ind2.getGene(4) + " " + ind2.getGene(5));

        int randomCross = (rand.nextInt(6)) + 1;
        int i;
        if(randomCross == 6){ randomCross = 5;}
        if(randomCross == 0){ randomCross = 1;}
        //System.out.println("RAND = " + randomCross);
        for(i=0;i<randomCross;i++){
            newIndiv[0].setGene(i, ind1.getGene(i));
            newIndiv[1].setGene(i, ind2.getGene(i));
        }
       // System.out.println("AIIII = " + i);
        for(; i<6;i++){
            newIndiv[0].setGene(i, ind2.getGene(i));
            newIndiv[1].setGene(i, ind1.getGene(i));
        }
       // System.out.println("AFTER");
       // System.out.println("FIR");
       // System.out.println(newIndiv[0].getGene(0) + " " + newIndiv[0].getGene(1) + " " + newIndiv[0].getGene(2) + " " + newIndiv[0].getGene(3) + " " + newIndiv[0].getGene(4) + " " + newIndiv[0].getGene(5));
       // System.out.println("SEC");
       // System.out.println(newIndiv[1].getGene(0) + " " + newIndiv[1].getGene(1) + " " + newIndiv[1].getGene(2) + " " + newIndiv[1].getGene(3) + " " + newIndiv[1].getGene(4) + " " + newIndiv[1].getGene(5));
        return newIndiv;
    }

    private static double[] datX()
    {
       int i = 0;
       double[] Xdata = new double[577];
       String line;
       try{
           BufferedReader input = new BufferedReader(new FileReader( "datfile.dat" ) );
           while((line = input.readLine()) != null){
               // System.out.println(i);
               // System.out.println(line);
               String []tokens = line.split("\\s+");
               double x = Double.parseDouble(tokens[0]);
               //System.out.println(x);
               Xdata[i] = x;
               i++;
            }
           input.close();
       }catch(IOException e){
           System.out.println(e);
        }
      
      
       return Xdata;
    }
    
    private static double[] datY()
    {
       int i = 0;
       double[] Ydata = new double[577];
       String line;
       try{
           BufferedReader input = new BufferedReader(new FileReader( "datfile.dat" ) );
           while((line = input.readLine()) != null){
               // System.out.println(i);
               // System.out.println(line);
               String []tokens = line.split("\\s+");
               double y = Double.parseDouble(tokens[1]);
               //System.out.println(y);
               Ydata[i] = y;
               i++;
            }
           input.close();
       }catch(IOException e){
           System.out.println(e);
        }
      
       
       return Ydata;
    }
}
