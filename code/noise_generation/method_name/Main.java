import java.io.File;

public class Main {
    public static void main(String[] args) {
        /*
         * noise type -> Y_Change_MethodName/X_Remove_Statement/X_Method_Variable
         * root folder for input  -> '~/methods'
         * root folder for output -> '~/noisy_methods'
         *
         * extracted single method of project should be in 'methods' folder
         * separate folder for each refactoring will be created in 'noisy_methods/noise_type' folder
         */

        String noiseType = String.valueOf(args[0]);
        File rootInputPath  = new File(args[1]);
        File rootOutputPath = new File(args[2]);
        rootOutputPath = new File(rootOutputPath, noiseType);

        File[] datasetPaths = rootInputPath.listFiles(File::isDirectory);
        if (datasetPaths != null) {
            for (Double noiseLimit : Common.NOISE_LIMITS) {
                for (File datasetPath : datasetPaths) {
                    String datasetName = datasetPath.getName();
                    for (String partitionName : Common.PARTITION_NAMES) {
                        new NoiseHandler(rootInputPath, rootOutputPath,
                                datasetName, partitionName,
                                noiseLimit, noiseType).call();
                    }
                }
            }
        } else {
            System.out.println("Project not found!");
        }
    }
}
