## Uso

This Python script compares two CSV files and finds the differences between them.:

```bash
python compare_csvs.py <file1> <file2> <delimiter> [--identifier <id_column>] [--merge_option <merge_column>] [--columns <excluded_columns>] [--output <output_file>]

Examples:
# Compare values ​​in the ID column
python3 reporting_compare.py file1.csv --file2 file2.csv '|' --identifier 'ID' --merge_option default

# Show records that are only in the left file
python3 reporting_compare.py file1.csv --file2 file2.csv '|' --identifier 'ID' --merge_option left_only

# Show records that are only in the right file
python3 reporting_compare.py file1.csv --file2 file2.csv '|' --identifier 'ID' --merge_option right_only

# Show records that are in both files
python3 reporting_compare.py file1.csv --file2 file2.csv '|' --identifier 'ID' --merge_option both

# Exclude columns 0, 3 and 4 when comparing
python3 reporting_compare.py file1.csv --file2 file2.csv '|' --identifier 'ID' --merge_option default --columns "0 3 4"

# Find duplicates in file
python3 main.py file1.csv '|'
```


## Comparing CSV files in Python

This Python code compares two CSV files and identifies the differences between them. It can be used to compare datasets, detect discrepancies, and ensure data consistency.

## Input arguments

The code requires the following input arguments to function properly:

* `file1`: Path to the first CSV file to be compared
* `delimiter`: Delimiter character used in the CSV files

## Optional arguments

The code also supports the following optional arguments for further customization:

* `--file2`: Path to the second CSV file to be compared
* `--identifier`: Column(s) to order the comparison results by
* `--merge_option`: Comparison option (left_only, right_only, both, or default)
* `--columns`: Space-separated list of column indices to exclude from the comparison
* `--output`: Name of the output file to store the comparison results

## Code breakdown

The code is divided into the following functions:

* `dataframe_create()`: Reads the two CSV files into Pandas DataFrames and optionally drops specified columns.
* `write_duplicates_output_file()`
Writes a CSV file with the duplicates found to a DataFrame and displays the total number of duplicates in the console.
* `remove_duplicates()`
Remove duplicates from a DataFrame.
* `dataset_difference()`: Performs the actual comparison between the two DataFrames. Creates a merged DataFrame and filters based on the chosen comparison option. Then, sorts the results by the specified columns and saves them to the output file (if provided).
* `handle_types()`: Handles missing values and converts values to strings for printing.
* `find_differences()`: Identifies and extracts the differences between corresponding rows in a group. Creates a mask indicating the columns with differences and extracts the original and different values for those columns. Then, constructs a DataFrame containing the identified differences.
* `main()`: Parses arguments, calls other functions to perform the comparison, and prints the results.

## Addressing warnings and errors

The provided code addresses two FutureWarnings and an error related to multi-dimensional indexing:

* **FutureWarning: `observed=False` Deprecation:** To avoid this warning and maintain the current behavior, explicitly pass `observed=False` to the `groupby()` method.
* **FutureWarning: `DataFrame.applymap` Deprecation:** Replace the `applymap()` call with `map()`.
* **Error: Multi-dimensional Indexing:** Convert the DataFrame to a NumPy array before indexing using the `to_numpy()` method.

## Conclusion

The provided Python code provides a comprehensive tool for comparing CSV files and identifying the differences between them. It allows for flexible comparison options, handles missing values, and provides detailed information about the differences.

## Additional details

* The `option` argument is used to specify what type of differences should be searched for. The available options are:
    * `left_only`: Only shows the differences in the data from the first file.
    * `right_only`: Only shows the differences in the data from the second file.
    * `both`: Shows all differences, including those that are present in both files.
    * `default`: Shows all differences, except those that are present in both files.
* The `handle_types()` function is used to convert the values to strings for printing. This is necessary for NaN values to be printed correctly.
* The `find_differences()` function uses a mask to identify the columns with differences. This mask is created using the `isna()` method to check if the values in the columns are NaN.

* -------------------------------------------------------------------------------------------------------------------------------------

# Español

# Comparación de archivos CSV

Este script en Python compara dos archivos CSV y encuentra las diferencias entre ellos.

## Requisitos
- Asegúrate de tener la biblioteca `pandas` instalada. Puedes instalarla ejecutando `pip install pandas`.
- Además, se utiliza la biblioteca `tabulate` para imprimir tablas en la consola. Puedes instalarla con `pip install tabulate`.

## Uso

El script se ejecuta desde la línea de comandos con los siguientes comandos:

```bash
python compare_csvs.py <file1> <file2> <delimiter> [--identifier <id_column>] [--merge_option <merge_column>] [--columns <excluded_columns>] [--output <output_file>]

Examples:
# Comparar valores en la columna ID
python3 reporting_compare.py file1.csv --file2 file2.csv '|' --identifier 'ID' --merge_option default

# Mostrar registros que solo están en el archivo izquierdo
python3 reporting_compare.py file1.csv --file2  file2.csv '|' --identifier 'ID' --merge_option left_only

# Mostrar registros que solo están en el archivo derecho
python3 reporting_compare.py file1.csv --file2 file2.csv '|' --identifier 'ID' --merge_option right_only

# Mostrar registros que están en ambos archivos
python3 reporting_compare.py file1.csv --file2 file2.csv '|' --identifier 'ID' --merge_option both

# Excluir columnas 0, 3 y 4 al realizar la comparación
python3 reporting_compare.py file1.csv f--file2 file2.csv '|' --identifier 'ID' --merge_option default --columns "0 3 4"

# Encontrar duplicados en el archivo
python3 main.py file1.csv '|'
```

## Comparación de archivos CSV en Python

Este código de Python compara dos archivos CSV y identifica las diferencias entre ellos. Se puede utilizar para comparar conjuntos de datos, detectar discrepancias y garantizar la coherencia de los datos.

## Argumentos de entrada

El código requiere los siguientes argumentos de entrada para funcionar correctamente:

* `file1`: Ruta al primer archivo CSV a comparar
* `delimiter`: Caracter delimitador utilizado en los archivos CSV

## Argumentos opcionales

El código también admite los siguientes argumentos opcionales para una mayor personalización:

* `--file2`: Ruta al segundo archivo CSV a comparar
* `--identifier`: Columna(s) para ordenar los resultados de la comparación
* `--merge_option`: Opción de comparación (left_only, right_only, both, o default)
* `--columns`: Lista separada por espacios de índices de columnas para excluir de la comparación
* `--output`: Nombre del archivo de salida para almacenar los resultados de la comparación

## Desglose del código

El código se divide en las siguientes funciones:

* `dataframe_create()`: Lee los archivos CSV y convierte a DataFrames de Pandas y, opcionalmente, elimina columnas especificadas.
* `write_duplicates_output_file()`: Escribe un archivo CSV con los duplicados encontrados en un DataFrame y muestra el número total de duplicados en la consola.
* `remove_duplicates()`: Elimina duplicados de un DataFrame.
* `dataset_difference()`: Realiza la comparación real entre los dos DataFrames. Crea un DataFrame fusionado y filtra según la opción de comparación elegida. Luego, ordena los resultados por las columnas especificadas y los guarda en el archivo de salida (si se proporciona).
* `manejar_tipo()`: Maneja los valores perdidos y convierte los valores a cadenas para imprimirlos.
* `encontrar_diferencias()`: Identifica y extrae las diferencias entre las filas correspondientes en un grupo. Crea una máscara que indica las columnas con diferencias y extrae los valores originales y diferentes para esas columnas. Luego, construye un DataFrame que contiene las diferencias identificadas.
* `main()`: Analiza los argumentos, llama a otras funciones para realizar la comparación e imprime los resultados.

## Abordando advertencias y errores

El código proporcionado aborda dos advertencias futuras y un error relacionado con el índice multidimensional:

* **FutureWarning: `observed=False` Deprecation:** Para evitar esta advertencia y mantener el comportamiento actual, pase explícitamente `observed=False` al método `groupby()`.
* **FutureWarning: `DataFrame.applymap` Deprecation:** Reemplace la llamada a `applymap()` con `map()`.
* **Error: Multi-dimensional Indexing:** Convierta el DataFrame en una matriz NumPy antes de indexarlo usando el método `to_numpy()`.

## Conclusión

El código de Python proporcionado una herramienta integral para comparar archivos CSV e identificar las diferencias entre ellos. Permite opciones de comparación flexibles, maneja valores perdidos y proporciona información detallada sobre las diferencias.

## Algunos detalles adicionales

* El argumento `option` se utiliza para especificar qué tipo de diferencias se deben buscar. Las opciones disponibles son:
    * `left_only`: Solo se muestran las diferencias en los datos del primer archivo.
    * `right_only`: Solo se muestran las diferencias en los datos del segundo archivo.
    * `both`: Se muestran todas las diferencias, incluidas las que están presentes en ambos archivos.
    * `default`: Se muestran todas las diferencias, excepto las que están presentes en ambos archivos.
* La función `manejar_tipo()` se utiliza para convertir los valores a cadenas para imprimirlos. Esto es necesario para que los valores NaN se impriman correctamente.
* La función `encontrar_diferencias()` utiliza una máscara para identificar las columnas con diferencias. Esta máscara se crea utilizando el método `isna()` para comprobar si los valores de las columnas son NaN.
