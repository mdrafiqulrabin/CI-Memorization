import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.stmt.Statement;
import com.github.javaparser.ast.visitor.TreeVisitor;
import org.apache.commons.io.FileUtils;

import java.io.File;
import java.util.*;
import java.util.concurrent.Callable;

public class NoiseHandler implements Callable<Void> {

    NoiseHandler(File rootInputPath, File rootOutputPath,
                 String datasetName, String partitionName, Double noiseLimit) {
        Common.ROOT_INPUT_PATH = rootInputPath;
        Common.ROOT_OUTPUT_PATH = rootOutputPath;
        Common.DATASET_NAME = datasetName;
        Common.PARTITION_NAME = partitionName;
        Common.NOISE_LIMIT = noiseLimit;
    }

    @Override
    public Void call() {
        inspectDataset();
        return null;
    }

    private void inspectDataset() {
        File input_dir = new File(Common.ROOT_INPUT_PATH, Common.DATASET_NAME + "/" + Common.PARTITION_NAME);
        ArrayList<File> allJavaFiles = new ArrayList<>(
                FileUtils.listFiles(input_dir, new String[]{"java"}, true)
        );
        System.out.println(input_dir + " : " + allJavaFiles.size());

        Map<String, ArrayList<File>> methodNameToFiles = Common.getMethodNameToFiles(allJavaFiles);
        ArrayList<String> uniqueMethodNames = new ArrayList<>();
        uniqueMethodNames = Common.getAllMethodNames(allJavaFiles, true);

        for (String methodName : methodNameToFiles.keySet()) {
            if (methodName.isEmpty()) continue;
            ArrayList<File> methodJavaFiles = methodNameToFiles.get(methodName);
            int noiseIdx = (int) (Common.NOISE_LIMIT * methodJavaFiles.size());
            String strNoiseLimit = (int) Math.round(Common.NOISE_LIMIT * 100) + "_percent";
            createNoisyData(methodName, noiseIdx, methodJavaFiles, uniqueMethodNames, strNoiseLimit);
        }
    }

    private void createNoisyData(String methodName, int noiseIdx, ArrayList<File> methodJavaFiles,
                                 ArrayList<String> uniqueMethodNames, String strNoiseLimit) {
        Collections.shuffle(methodJavaFiles);
        for (int i = 0; i < methodJavaFiles.size(); i++) {
            File javaFile = methodJavaFiles.get(i);
            CompilationUnit com = Common.getParseUnit(javaFile);
            if (com == null) return;
            changeRandomMethodName(methodName, noiseIdx, uniqueMethodNames, strNoiseLimit, i, javaFile, com);
        }
    }

    private void changeRandomMethodName(String methodName, int noiseIdx, ArrayList<String> uniqueMethodNames,
                                        String strNoiseLimit, int i, File javaFile, CompilationUnit com) {
        String newMethodName = methodName;
        if (i < noiseIdx) {
            List<String> targetMethodNames = new ArrayList<>(uniqueMethodNames);
            targetMethodNames.remove(methodName);
            Collections.shuffle(targetMethodNames);
            newMethodName = targetMethodNames.get(new Random().nextInt(targetMethodNames.size()));
            MethodDeclaration md = Common.getMethodDeclaration0(com);
            if (md != null && !newMethodName.isEmpty()) {
                md.setName(newMethodName);
            }
        }
        Common.saveModification(com, javaFile, strNoiseLimit);
    }

}
