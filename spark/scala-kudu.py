# Kudu Integration with Spark

# Spark 1.x - Use the kudu-spark_2.10 artifact if you are using Spark 1.x with Scala 2.10:
spark-shell --packages org.apache.kudu:kudu-spark_2.10:1.1.0

# Spark 2.x - Use the kudu-spark2_2.11 artifact if you are using Spark 2.x with Scala 2.11:
spark2-shell --packages org.apache.kudu:kudu-spark2_2.11:1.4.0

Then import kudu-spark and create a dataframe as demonstrated in the following sample code. In the following example, replace <kudu.master> with the actual hostname of the host running a Kudu master service, and <kudu_table> with the name of a pre-existing table in Kudu.

import org.apache.kudu.spark.kudu._

// Read a table from Kudu 
val df = spark.sqlContext.read.options(Map("kudu.master" -> "<kudu.master>:7051","kudu.table" -> "<kudu_table>")).kudu

// Query <kudu_table> using the Spark API...
df.select("id").filter("id" >= 5).show()

// ...or register a temporary table and use SQL
df.registerTempTable("<kudu_table>")
val filteredDF = sqlContext.sql("select id from <kudu_table> where id >= 5").show()

// Use KuduContext to create, delete, or write to Kudu tables
val kuduContext = new KuduContext("<kudu.master>:7051", sqlContext.sparkContext)

// Create a new Kudu table from a dataframe schema
// NB: No rows from the dataframe are inserted into the table
kuduContext.createTable("test_table", df.schema, Seq("key"), new CreateTableOptions().setNumReplicas(1))

// Insert data
kuduContext.insertRows(df, "test_table")

// Delete data
kuduContext.deleteRows(filteredDF, "test_table")

// Upsert data
kuduContext.upsertRows(df, "test_table")

// Update data
val alteredDF = df.select("id", $"count" + 1)
kuduContext.updateRows(filteredRows, "test_table"

// Data can also be inserted into the Kudu table using the data source, though the methods on KuduContext are preferred
// NB: The default is to upsert rows; to perform standard inserts instead, set operation = insert in the options map
// NB: Only mode Append is supported
df.write.options(Map("kudu.master"-> "<kudu.master>:7051", "kudu.table"-> "test_table")).mode("append").kudu

// Check for the existence of a Kudu table
kuduContext.tableExists("another_table")

// Delete a Kudu table
kuduContext.deleteTable("unwanted_table")