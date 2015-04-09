package predictpkg;

import java.io.IOException;
import java.lang.ProcessBuilder.Redirect;

public class Classifier {
	
	public static void predict(String pathPyFiles) {
		// TODO Auto-generated method stub
		String pythonScriptPath = pathPyFiles+"online-predict.py";
		System.out.println("pythonScriptPath");
		System.out.println(pythonScriptPath);
		try {
			ProcessBuilder pb = new ProcessBuilder("/usr/bin/python",pythonScriptPath);
	        pb.redirectOutput(Redirect.INHERIT);
	        Process p = pb.start();
	        int success = p.waitFor();
	        System.out.println("waitFor");
			System.out.println(success);
		} catch (IOException | InterruptedException e) {
			// TODO Auto-generated catch block
			System.out.println("Predict Failed!");
			e.printStackTrace();
		}
	}

}
