// See https://aka.ms/new-console-template for more information
using System;
using System.IO;
using System.Threading.Tasks;

namespace DateTimeFetcher
{
    class Program
    {
        static async Task Main(string[] args)
        {
            try
            {
                // Get the current date and time
                DateTime currentTime = DateTime.Now;
                Console.WriteLine("Current date and time: " + currentTime);

                // Format the current date and time as a string for the file name
                string formattedDateTime = currentTime.ToString("dd-MM-yyyy-HH-mm-ss");

                // Prepare the content to write to the file
                string content = $"Current Date and Time: {currentTime:yyyy-MM-dd HH:mm:ss}";

                // Define the file name with the formatted date and time
                string fileName = $"{formattedDateTime}.txt";

                // Write the content to a file in the current directory
                using (StreamWriter writer = new StreamWriter(fileName))
                {
                    await writer.WriteAsync(content);
                }

                Console.WriteLine($"Date and time written to {fileName}");
            }
            catch (Exception e)
            {
                Console.WriteLine($"Error fetching date and time: {e.Message}");
            }
        }
    }
}
