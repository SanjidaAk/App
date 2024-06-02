import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.TreeMap;

public class WordCount {

    public static void main(String[] args) {
        String filePath = "/uploads/fr.txt"; 
        count(filePath);
    }

    public static void count(String filePath) {
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            StringBuilder text = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                text.append(line).append(" ");
            }

            
            String cleanedText = text.toString().replaceAll("[\\p{Punct}]", "");

            
            String[] words = cleanedText.split("\\s+");

            
            Map<String, Integer> wordCount = new HashMap<>();
            for (String word : words) {
                wordCount.put(word, wordCount.getOrDefault(word, 0) + 1);
            }

            Map<String, Integer> sortedWordCount = new TreeMap<>(wordCount);

            for (Map.Entry<String, Integer> entry : sortedWordCount.entrySet()) {
                System.out.println(entry.getKey() + ": " + entry.getValue());
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
