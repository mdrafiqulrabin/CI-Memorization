import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.stmt.BlockStmt;
import com.github.javaparser.ast.stmt.EmptyStmt;
import com.github.javaparser.ast.stmt.Statement;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

@SuppressWarnings({"WeakerAccess", "unused"})
public final class Common {

    static final String Y_NOISE_CHANGE_LABEL = "Y_Change_MethodName";
    static final String X_NOISE_REMOVE_STMT = "X_Remove_Statement";
    static final String X_NOISE_METHOD_VAR = "X_Method_Variable";

    static File ROOT_INPUT_PATH = new File("");
    static File ROOT_OUTPUT_PATH = new File("");
    static String DATASET_NAME = "";
    static String PARTITION_NAME = "";
    static Double NOISE_LIMIT = 0.0;
    static String NOISE_TYPE = "";

    static List<String> PARTITION_NAMES = Arrays.asList("training");
    static List<Double> NOISE_LIMITS = Arrays.asList(0.25, 0.50, 0.75, 1.00);

    static CompilationUnit getParseUnit(File javaFile) {
        CompilationUnit root = null;
        try {
            String txtCode = new String(Files.readAllBytes(javaFile.toPath()));
            if(!txtCode.startsWith("class")) txtCode = "class T { \n" + txtCode + "\n}";
            //StaticJavaParser.getConfiguration().setAttributeComments(false);
            root = StaticJavaParser.parse(txtCode);
        } catch (Exception ignore) {}
        return root;
    }

    static MethodDeclaration getMethodDeclaration0(CompilationUnit com) {
        MethodDeclaration md = null;
        try {
            md = com.findAll(MethodDeclaration.class).get(0);
        } catch (Exception ignore) {}
        return md;
    }

    static String getMethodName(File javaFile) {
        String methodName = "";
        CompilationUnit com = Common.getParseUnit(javaFile);
        if (com != null) {
            MethodDeclaration md = Common.getMethodDeclaration0(com);
            if (md != null) {
                methodName = md.getName().asString();
            }
        }
        return methodName;
    }

    static ArrayList<String> getAllMethodNames(ArrayList<File> javaFiles, boolean unique) {
        ArrayList<String> listOfMethodNames = new ArrayList<>();
        for(File javaFile: javaFiles) {
            CompilationUnit com = Common.getParseUnit(javaFile);
            if (com != null) {
                MethodDeclaration md = Common.getMethodDeclaration0(com);
                if (md != null) {
                    String methodName = md.getNameAsString();
                    listOfMethodNames.add(methodName);
                }
            }
        }
        if(unique) {
            Set<String> setOfMethodNames = new LinkedHashSet<>(listOfMethodNames);
            listOfMethodNames.clear();
            listOfMethodNames.addAll(setOfMethodNames);
        }
        return listOfMethodNames;
    }

    static Map<String, ArrayList<File>> getMethodNameToFiles(ArrayList<File> javaFiles) {
        Map<String, ArrayList<File>> methodNameToFiles = new HashMap<>();
        for (File javaFile : javaFiles) {
            String methodName = Common.getMethodName(javaFile);
            if (methodName.isEmpty()) continue;
            if (methodNameToFiles.containsKey(methodName)) {
                ArrayList<File> listJavaFile = methodNameToFiles.get(methodName);
                listJavaFile.add(javaFile);
            } else {
                ArrayList<File> listJavaFile = new ArrayList<>();
                listJavaFile.add(javaFile);
                methodNameToFiles.put(methodName, listJavaFile);
            }
        }
        return methodNameToFiles;
    }

    static ArrayList<Path> getFilePaths(String rootPath) {
        ArrayList<Path> listOfPaths = new ArrayList<>();
        final FilenameFilter filter = (dir, name) -> dir.isDirectory() && name.toLowerCase().endsWith(".txt");
        File[] listOfFiles = new File(rootPath).listFiles(filter);
        if (listOfFiles == null) return new ArrayList<>();
        for (File file : listOfFiles) {
            Path codePath = Paths.get(file.getPath());
            listOfPaths.add(codePath);
        }
        return listOfPaths;
    }

    static boolean isSingleStatement(Node node) {
        return node != null && !(node instanceof EmptyStmt || node instanceof BlockStmt)
                && node.findAll(Statement.class).size() == 1;
    }

    static void saveModification(CompilationUnit com, File javaFile, String strNoiseLimit) {
        String file_path  = javaFile.getPath().replaceFirst(Common.ROOT_INPUT_PATH.toString(), "");
        String output_dir = new File(Common.ROOT_OUTPUT_PATH, strNoiseLimit + file_path).toString();
        MethodDeclaration md = Common.getMethodDeclaration0(com);
        if (md != null) {
            Common.writeSourceCode(md, output_dir);
        }
    }

    static void writeSourceCode(MethodDeclaration md, String codePath) {
        File targetFile = new File(codePath).getParentFile();
        if (targetFile.exists() || targetFile.mkdirs()) {
            try (PrintStream ps = new PrintStream(codePath)) {
                String tfSourceCode = md.toString();
                ps.println(tfSourceCode);
            } catch (FileNotFoundException ex) {
                ex.printStackTrace();
            }
        }
    }
}
