import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.Parameter;
import com.github.javaparser.ast.body.VariableDeclarator;
import com.github.javaparser.ast.expr.SimpleName;
import com.github.javaparser.ast.visitor.TreeVisitor;

import java.util.ArrayList;

public class VariableRenaming {

    public CompilationUnit inspectSourceCode(CompilationUnit oldCom) {
        ArrayList<Node> variableNodes = locateVariableRenaming(oldCom);
        // System.out.println("TargetVariable : " + variableNodes);

        String oldVariableName = "";
        int maxCount = 0;
        for (Node varNode : variableNodes) {
            int count = oldCom.findAll(SimpleName.class, node -> node.toString().equals(varNode.toString())).size();
            if (count > maxCount) {
                maxCount = count;
                oldVariableName = varNode.toString();
            }
        }

        String newVariableName = "";
        MethodDeclaration md = Common.getMethodDeclaration0(oldCom);
        if (md != null) {
            newVariableName = md.getNameAsString();
        }

        return applyTransformation(oldCom, oldVariableName, newVariableName);
    }

    private ArrayList<Node> locateVariableRenaming(CompilationUnit com) {
        ArrayList<Node> variableNodes = new ArrayList<>();
        new TreeVisitor() {
            @Override
            public void process(Node node) {
                if (isTargetVariable(node, com)) {
                    variableNodes.add(node);
                }
            }
        }.visitPreOrder(com);
        return variableNodes;
    }

    private boolean isTargetVariable(Node node, CompilationUnit com) {
        return (node instanceof SimpleName &&
                (node.getParentNode().orElse(null) instanceof Parameter
                        || node.getParentNode().orElse(null) instanceof VariableDeclarator));
    }

    private CompilationUnit applyTransformation(CompilationUnit com, String oldName, String newName) {
        new TreeVisitor() {
            @Override
            public void process(Node node) {
                if (node.toString().equals(oldName)) {
                    if (node instanceof SimpleName
                            && !(node.getParentNode().orElse(null) instanceof MethodDeclaration)
                            && !(node.getParentNode().orElse(null) instanceof ClassOrInterfaceDeclaration)) {
                        ((SimpleName) node).setIdentifier(newName);
                    }
                }
            }
        }.visitPreOrder(com);
        return com;
    }
}
