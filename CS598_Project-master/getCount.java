import java.io.*;
import java.util.*;

public class getCount{
	public static void main(String[] args) {
		try {
			HashMap<String, Integer> map = new HashMap<String, Integer>();
			BufferedReader br = new BufferedReader(new FileReader("tweets.txt"));

			String curLine;

			while ((curLine = br.readLine()) != null) {
				String[] cur = curLine.split("\t");
				String tag = "";

				if(cur.length > 1 && cur[0].split(" ").length > 1){
					tag = cur[0].split(" ")[1];
				}

				if(!map.containsKey(tag)){
					map.put(tag, 1);
				} else{
					map.put(tag, map.get(tag) + 1);
				}
			}

			File file = new File("count.txt");

			// if file doesnt exists, then create it
			if (!file.exists()) {
				file.createNewFile();
			}

			FileWriter fw = new FileWriter(file.getAbsoluteFile());
			BufferedWriter bw = new BufferedWriter(fw);

			for(Map.Entry<String, Integer> entry : map.entrySet()){
				String hashTag = entry.getKey();

				if(hashTag.length() > 0 && !hashTag.startsWith("https")){
					String content = hashTag + ":" + entry.getValue() + "\n";
					bw.write(content);
				}
			}

			bw.close();

		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}