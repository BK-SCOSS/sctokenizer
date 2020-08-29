import java.util.HashMap;
import java.util.Map.Entry;

class Main {
  public static void main(String[] args) {

    // create a hashmap
    HashMap<String, Integer> numbers = new HashMap<>();
    numbers.put("One", 1);
    numbers.put("Two", 2);
    numbers.put("Three", 3);
    System.out.println("HashMap: " + numbers);

    // value whose key is to be searched
    Integer value = 3;

    // iterate each entry of hashmap
    for(Entry<String, Integer> entry: numbers.entrySet()) {

      // if give value is equal to value from entry
      // print the corresponding key
      if(entry.getValue() == value) {
        System.out.println("The key for value " + value + " is " + entry.getKey());
        break;
      }
    }
  }
}