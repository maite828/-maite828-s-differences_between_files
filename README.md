# CSV File Comparer

This code compares two CSV files and finds the differences between them. The code can be used to compare files of any size or format.

## Overview

The code works as follows:

1. The data from the two CSV files is read.
2. The data from the two CSV files is compared.
3. The differences between the two CSV files are found.
4. Find duplicate records in a file.

## Usage examples

### To compare two CSV files, you can use the following commands:
* `python3 main.py <file1> [--file2 <file2>] <delimiter> [--identifier <id_column>] [--merge_option <merge_column>] [--cols_index <excluded_columns>] [--output <output_file>]`

Examples:
```bash
# Compare values in the ID column
python3 main.py file1.csv --file2 file2.csv '|' --identifier 'ID' --merge_option default
```

```bash
# Show records that are only in the left file
python3 main.py file1.csv --file2  file2.csv '|' --identifier 'ID' --merge_option left_only
```

```bash
# Show records that are only in the right file
python3 main.py file1.csv --file2 file2.csv '|' --identifier 'ID' --merge_option right_only
```

```bash
# Show records that are in both files
python3 main.py file1.csv --file2 file2.csv '|' --identifier 'ID' --merge_option both
```

```bash
# Exclude columns 0, 3, and 4 when performing the comparison
python3 main.py file1.csv --file2 file2.csv '|' --identifier 'ID' --merge_option default --cols_index "0 3 4"
```

### Find duplicates in the file
* `python3 main.py <file1> <delimiter>`

Examples:
```bash
python3 main.py file1.csv '|'
```
```bash
# Finding duplicates in the file, 'cols_index' will allow us to choose the range of columns to display.
python3 main.py file1.csv '|' --cols_index "3-6"
```

## Description

This document provides examples of how to use the `main.py` script to compare two CSV files or find duplicates in a file.

## Command line arguments

The `reporting_compare.py` script takes the following command line arguments:

* `file1` and `--file2`: The names of the two CSV files to be compared or the name of the file to be searched for duplicates.
* `delimiter`: The delimiter used to separate the columns in the CSV files.
* `--identifier`: The name of the column to use to identify duplicate records.
* `--merge_option`: The option to use when merging records with duplicate identifiers.
* `--cols_index`: A comma-separated list of columns to exclude from the comparison.

## Merge options

The `--merge_option` argument can have one of the following values:

* `default`: Merge records with duplicate identifiers by combining the values of all columns.
* `left_only`: Keep only the records from the left file.
* `right_only`: Keep only the records from the right file.
* `both`: Keep all records, including duplicates.

## Input arguments

To find duplicates in a file, use the following command:

* `file1`: **Path to the first CSV file to compare**
* `delimiter`: **Delimiter character used in the CSV files**

## Optional arguments

The code also supports the following optional arguments for greater customization:

* `--file2`: **Path to the second CSV file to compare**
* `--identifier`: **Column(s) to use to sort the results of the comparison**
* `--merge_option`: **Comparison option (left_only, right_only, both, or default)**
* `--cols_index`: **List of column indices separated by spaces to exclude from the comparison**
* `--output`: **Name of the output file to store the results of the comparison**

## Functions

The code contains the following functions:

* `parse_args()`: Parses command-line arguments.
* `process_single_file()`: Compares a single CSV file.
* `process_two_files()`: Compares two CSV files.
* `read_csv()`: Reads a CSV file.
* `compare_dt()`: Compares two DataFrames.
* `find_differences()`: Finds the differences between two DataFrames.

## Input and output

The input and output of each function is described below:

**`parse_args()`**

* Input:
    * `file1`: Path to the first CSV file.
    * `file2`: Path to the second CSV file.
    * `delimiter`: Delimiter used in the CSV files.
    * `identifier`: Column(s) to order the results.
    * `merge_option`: Comparison option: `left_only`, `right_only`, `both`, or `default`.
    * `cols_index`: Columns to exclude (space-separated indices).
    * `output`: Output file name.
* Output:
    * `argparse.Namespace` object with the processed arguments.

**`process_single_file()`**

* Input:
    * `csv_handler`: `CSVHandler` object.
    * `data_comparator`: `DataComparator` object.
    * `arguments`: `argparse.Namespace` object with the processed arguments.
    * `base_path`: Path to the base directory.
* Output:
    None.

**`process_two_files()`**

* Input:
    * `csv_handler`: `CSVHandler` object.
    * `data_comparator`: `DataComparator` object.
    * `arguments`: `argparse.Namespace` object with the processed arguments.
    * `base_path`: Path to the base directory.
* Output:
    None.

**`read_csv()`**

* Input:
    * `csv_handler`: `CSVHandler` object.
    * `path`: Path to the CSV file.
    * `delimiter`: Delimiter used in the CSV file.
    * `cols`: Columns to exclude (space-separated indices).
* Output:
    `DataFrame` with the data from the CSV file.

**`compare_dt()`**

* Input:
    * `df1`: `DataFrame` with the data from the first CSV file.
    * `df2`: `DataFrame` with the data from the second CSV file.
    * `identifier`: Column(s) to order the results.
    * `merge_option`: Comparison option: `left_only`, `right_only`, `both`, or `default`.
* Output:
    `DataFrame` with the differences between the two DataFrames.

**`find_differences()`**

* Input:
    * `df`: `DataFrame` with the differences between the two DataFrames.
    * `identifier`: Column(s) to order the results.
* Output:
    `DataFrame` with detailed differences between the two DataFrames


## Conclusion

The Python code provided is a comprehensive tool for comparing CSV files and identifying differences between them. It allows for flexible comparison options, handles missing values, and provides detailed information about the differences.

## Additional details

* The `option` argument is used to specify what type of differences to look for. The available options are:
    * `left_only`: **Only shows differences in the data of the first file**
    * `right_only`: **Only shows differences in the data of the second file**
    * `both`: **Shows all differences, including those that are present in both files**
    * `default`: **Shows all differences except those that are present in both files**



# Español
## Comparador de archivos CSV

Este código compara dos archivos CSV y encuentra las diferencias entre ellos. El código se puede utilizar para comparar archivos de cualquier tamaño o formato.

## Descripción general

El código funciona de la siguiente manera:

1. Se leen los datos de los dos archivos CSV.
2. Se comparan los datos de los dos archivos CSV.
3. Se encuentran las diferencias entre los dos archivos CSV.
4. Busca registros duplicados en un archivo.

## Ejemplos de uso

### Para comparar dos archivos CSV, puedes utilizar los siguientes comandos:
* `python3 main.py <file1> [--file2 <file2>] <delimiter> [--identifier <id_column>] [--merge_option <merge_column>] [--cols_index <excluded_columns>] [--output <output_file>]`

Examples:
```bash
# Comparar valores en la columna ID
python3 main.py file1.csv --file2 file2.csv '|' --identifier 'ID' --merge_option default
```

```bash
# Mostrar registros que solo están en el archivo izquierdo
python3 main.py file1.csv --file2  file2.csv '|' --identifier 'ID' --merge_option left_only
```

```bash
# Mostrar registros que solo están en el archivo derecho
python3 main.py file1.csv --file2 file2.csv '|' --identifier 'ID' --merge_option right_only
```

```bash
# Mostrar registros que están en ambos archivos
python3 main.py file1.csv --file2 file2.csv '|' --identifier 'ID' --merge_option both
```

```bash
# Excluir columnas 0, 3 y 4 al realizar la comparación
python3 main.py file1.csv --file2 file2.csv '|' --identifier 'ID' --merge_option default --cols_index "0 3 4"
```

### Para encontrar duplicados en un archivo usa el siguiente comando:
* `python3 main.py <file1> <delimiter>`

Examples:
```bash
# Encontrar duplicados en el archivo
python3 main.py file1.csv '|'
```
```bash
# Encontrar duplicados en el archivo, 'cols_index' nos permitirá elegir el rango de columnas a visualizar.
python3 main.py file1.csv '|' --cols_index "3-4"
```

## Argumentos de entrada

El código requiere los siguientes argumentos de entrada para funcionar correctamente:

* `file1`: Ruta al primer archivo CSV a comparar
* `delimiter`: Character delimitador utilizado en los archivos CSV

## Argumentos opcionales

El código también admite los siguientes argumentos opcionales para una mayor personalización:

* `--file2`: Ruta al segundo archivo CSV a comparar
* `--identifier`: Columna(s) para ordenar los resultados de la comparación
* `--merge_option`: Opción de comparación (left_only, right_only, both, o default)
* `--cols_index`: Lista separada por espacios de índices de columnas para excluir de la comparación
* `--output`: Nombre del archivo de salida para almacenar los resultados de la comparación

## Funciones

El código contiene las siguientes funciones:

* `parse_args()`: Parsea los argumentos de la línea de comandos.
* `process_single_file()`: Compara un solo archivo CSV.
* `process_two_files()`: Compara dos archivos CSV.
* `read_csv()`: Lee un archivo CSV.
* `compare_dt()`: Compara dos DataFrames.
* `find_differences()`: Encuentra las diferencias entre dos DataFrames.

## Entrada y salida

La entrada y salida de cada función se describe a continuación:

**`parse_args()`**

* Entrada:
    * `file1`: Ruta al primer archivo CSV.
    * `file2`: Ruta al segundo archivo CSV.
    * `delimiter`: Delimitador utilizado en los archivos CSV.
    * `identifier`: Columna(s) para ordenar los resultados.
    * `merge_option`: Opción de comparación: `left_only`, `right_only`, `both`, o `default`.
    * `cols`: Columnas para excluir (índices separados por espacios).
    * `output`: Nombre del archivo de salida.
* Salida:
    * Objeto `argparse.Namespace` con los argumentos procesados.

**`process_single_file()`**

* Entrada:
    * `csv_handler`: Objeto `CSVHandler`.
    * `data_comparator`: Objeto `DataComparator`.
    * `arguments`: Objeto `argparse.Namespace` con los argumentos procesados.
    * `base_path`: Ruta al directorio base.
* Salida:
    None.

**`process_two_files()`**

* Entrada:
    * `csv_handler`: Objeto `CSVHandler`.
    * `data_comparator`: Objeto `DataComparator`.
    * `arguments`: Objeto `argparse.Namespace` con los argumentos procesados.
    * `base_path`: Ruta al directorio base.
* Salida:
    None.

**`read_csv()`**

* Entrada:
    * `csv_handler`: Objeto `CSVHandler`.
    * `path`: Ruta al archivo CSV.
    * `delimiter`: Delimitador utilizado en el archivo CSV.
    * `cols`: Columnas para excluir (índices separados por espacios).
* Salida:
    `DataFrame` con los datos del archivo CSV.

**`compare_dt()`**

* Entrada:
    * `df1`: DataFrame con los datos del primer archivo CSV.
    * `df2`: DataFrame con los datos del segundo archivo CSV.
    * `identifier`: Columna(s) para ordenar los resultados.
    * `merge_option`: Opción de comparación: `left_only`, `right_only`, `both`, o `default`.
* Salida:
    `DataFrame` con las diferencias entre los dos DataFrames.

**`find_differences()`**

* Entrada:
    * `df`: DataFrame con las diferencias entre los dos DataFrames.
    * `identifier`: Columna(s) para ordenar los resultados.
* Salida:
    `DataFrame` con las diferencias detalladas entre los dos DataFrames.

## Conclusión

El código de Python proporcionado una herramienta integral para comparar archivos CSV e identificar las diferencias entre ellos. Permite opciones de comparación flexibles, maneja valores perdidos y proporciona información detallada sobre las diferencias.

## Algunos detalles adicionales

* El argumento `option` se utiliza para especificar qué tipo de diferencias se deben buscar. Las opciones disponibles son:
    * `left_only`: Solo se muestran las diferencias en los datos del primer archivo.
    * `right_only`: Solo se muestran las diferencias en los datos del segundo archivo.
    * `both`: Se muestran todas las diferencias, incluidas las que están presentes en ambos archivos.
    * `default`: Se muestran todas las diferencias, excepto las que están presentes en ambos archivos.
