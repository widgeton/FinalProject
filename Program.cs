
string[] LimitLengthOfStrings(string[] array, int length)
{
    int size = default;
    for (int i = 0; i < array.Length; i++)
        if(array[i].Length <= length) size++;

    string[] result = new string[size];
    int j = default;
    
    for (int i = 0; i < array.Length; i++)
    {
        if(array[i].Length <= length)
        {
            result[j] = array[i];
            j++;
        }
    }

    return result;
}

void ShowStrArray(string[] array)
{
    Console.Write("[");
    for (int i = 0; i < array.Length; i++)
    {
        if(i == array.Length - 1) Console.Write($"\"{array[i]}\"");
        else Console.Write($"\"{array[i]}\", ");
    }
    Console.Write("]");
    Console.WriteLine();
    
}

string[] array1 = {"Hello", "2", "world", ":-)"};
string[] newArray1 = LimitLengthOfStrings(array1, 3);
ShowStrArray(array1);
ShowStrArray(newArray1);
Console.WriteLine();

string[] array2 = {"1234", "1567", "-2", "computer science"};
string[] newArray2 = LimitLengthOfStrings(array2, 3);
ShowStrArray(array2);
ShowStrArray(newArray2);
Console.WriteLine();

string[] array3 = {"Russia", "Denmark", "Kazan"};
string[] newArray3 = LimitLengthOfStrings(array3, 3);
ShowStrArray(array3);
ShowStrArray(newArray3);
Console.WriteLine();