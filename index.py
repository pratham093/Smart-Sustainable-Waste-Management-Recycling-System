import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from decimal import Decimal
import matplotlib
matplotlib.use('TkAgg')

class WasteManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Waste Management Database System - Smart Visualizations")
        self.root.geometry("1000x750")

        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'newpassword', 
            'database': 'waste_management_system'
        }

        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        title_label = ttk.Label(main_frame, text="Waste Management Query System", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        menu_frame = ttk.LabelFrame(main_frame, text="Select Query Option", padding="10")
        menu_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        self.query_options = [
            "1. Total waste collected by zone (last month)",
            "2. Recycling rate by household",
            "3. Vehicle utilization analysis",
            "4. Outstanding violations and fines",
            "5. Staff performance metrics",
            "6. Waste type distribution analysis",
            "7. Route efficiency analysis",
            "8. Payment analysis by household",
            "9. Recycling center capacity analysis",
            "10. Collection schedule compliance",
            "11. Top performing routes",
            "12. Violation trends by month"
        ]

        self.query_visualizations = {
            1: ('bar', '📊 Bar Chart', 'Zone Comparison'),
            2: ('scatter', '⚡ Scatter Plot', 'Recycling Rate Distribution'),
            3: ('boxplot', '📦 Box Plot', 'Weight Distribution'),
            4: ('horizontal_bar', '📊 Horizontal Bar', 'Violations by Household'),
            5: ('grouped_bar', '📊 Grouped Bar', 'Staff Performance'),
            6: ('pie', '🥧 Pie Chart', 'Waste Type Distribution'),
            7: ('heatmap', '🔥 Heatmap', 'Route Efficiency Matrix'),
            8: ('stacked_bar', '📊 Stacked Bar', 'Payment Breakdown'),
            9: ('grouped_bar', '📊 Grouped Bar', 'Center Capacity'),
            10: ('line', '📈 Line Chart', 'Compliance Trends'),
            11: ('bar', '📊 Bar Chart', 'Top Routes Ranking'),
            12: ('area', '🎯 Area Chart', 'Violation Trends Over Time')
        }

        for i, option in enumerate(self.query_options):
            row = i // 3
            col = i % 3
            btn = ttk.Button(menu_frame, text=option, width=35,
                           command=lambda x=i+1: self.execute_query(x))
            btn.grid(row=row, column=col, padx=5, pady=5)

        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Label(control_frame, text="Or enter query number (1-12):").grid(row=0, column=0, padx=5)
        self.query_input = ttk.Entry(control_frame, width=10)
        self.query_input.grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="Execute", 
                  command=self.execute_from_input).grid(row=0, column=2, padx=5)

        self.viz_button = None
        self.viz_button_frame = ttk.Frame(control_frame)
        self.viz_button_frame.grid(row=0, column=3, padx=20)

        self.status_label = ttk.Label(control_frame, text="", font=('Arial', 10))
        self.status_label.grid(row=1, column=0, columnspan=4, pady=5)

        result_frame = ttk.LabelFrame(main_frame, text="Query Results", padding="10")
        result_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        self.result_text = scrolledtext.ScrolledText(result_frame, height=15, width=100)
        self.result_text.pack(fill=tk.BOTH, expand=True)

        self.last_results = None
        self.last_query_type = None

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
    def execute_from_input(self):
        try:
            query_num = int(self.query_input.get())
            if 1 <= query_num <= 12:
                self.execute_query(query_num)
            else:
                messagebox.showerror("Error", "Please enter a number between 1 and 12")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
    
    def execute_query(self, query_num):
        """Execute query based on selection (switch-case style)"""
        self.result_text.delete(1.0, tk.END)
        self.last_query_type = query_num

        queries = {
            1: """
                SELECT z.Name AS Zone_Name,
                       COUNT(DISTINCT cl.CollectionLogID) AS Collection_Count,
                       SUM(cl.TotalRouteWeight) AS Total_Weight_Collected
                FROM Zone z
                JOIN Route r ON z.ZoneID = r.ZoneID
                JOIN CollectionLog cl ON r.RouteID = cl.RouteID
                WHERE cl.CollectionDate >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
                GROUP BY z.ZoneID, z.Name
                ORDER BY Total_Weight_Collected DESC
            """,
            
            2: """
                SELECT h.Name AS Household_Name,
                       h.Address,
                       COUNT(CASE WHEN wt.Name = 'Recyclable' THEN 1 END) AS Recyclable_Bins,
                       COUNT(wb.BinID) AS Total_Bins,
                       ROUND(COUNT(CASE WHEN wt.Name = 'Recyclable' THEN 1 END) * 100.0 / 
                             COUNT(wb.BinID), 2) AS Recycling_Rate_Percentage
                FROM Household h
                LEFT JOIN WasteBin wb ON h.HouseholdID = wb.HouseholdID
                LEFT JOIN WasteType wt ON wb.WasteTypeID = wt.WasteTypeID
                GROUP BY h.HouseholdID, h.Name, h.Address
                ORDER BY Recycling_Rate_Percentage DESC
            """,
            
            3: """
                SELECT v.VehicleID,
                       v.Model,
                       v.Make,
                       v.LicensePlate,
                       v.Status,
                       v.Capacity,
                       COUNT(DISTINCT cl.CollectionLogID) AS Total_Collections,
                       COALESCE(AVG(cl.TotalRouteWeight), 0) AS Avg_Weight_Per_Collection,
                       COALESCE(SUM(cl.TotalRouteWeight), 0) AS Total_Weight_Collected,
                       CASE 
                           WHEN COUNT(cl.CollectionLogID) = 0 THEN 0
                           ELSE ROUND((AVG(cl.TotalRouteWeight) / v.Capacity) * 100, 2)
                       END AS Avg_Capacity_Usage_Percent,
                       CASE
                           WHEN v.Status = 'Maintenance' THEN 'Under Maintenance'
                           WHEN COUNT(cl.CollectionLogID) = 0 THEN 'Not Used'
                           WHEN AVG(cl.TotalRouteWeight) / v.Capacity > 0.8 THEN 'High Usage'
                           WHEN AVG(cl.TotalRouteWeight) / v.Capacity > 0.5 THEN 'Medium Usage'
                           ELSE 'Low Usage'
                       END AS Usage_Category
                FROM Vehicle v
                LEFT JOIN CollectionLog cl ON v.VehicleID = cl.VehicleID
                GROUP BY v.VehicleID, v.Model, v.Make, v.LicensePlate, v.Status, v.Capacity
                ORDER BY Total_Collections DESC
            """,
            
            4: """
                SELECT h.Name AS Household_Name,
                       h.Address,
                       COUNT(v.ViolationID) AS Total_Violations,
                       SUM(CASE WHEN v.Status = 'Pending' THEN 1 ELSE 0 END) AS Pending_Violations,
                       SUM(CASE WHEN v.Status = 'Pending' THEN v.FineAmount ELSE 0 END) AS Outstanding_Fines
                FROM Household h
                LEFT JOIN Violation v ON h.HouseholdID = v.HouseholdID
                GROUP BY h.HouseholdID, h.Name, h.Address
                HAVING Total_Violations > 0
                ORDER BY Outstanding_Fines DESC
            """,
            
            5: """
                SELECT s.StaffID,
                       s.Name,
                       s.Role,
                       COUNT(DISTINCT ls.CollectionLogID) AS Collections_Participated,
                       COUNT(DISTINCT cl.RouteID) AS Routes_Covered,
                       ROUND(AVG(cl.TotalRouteWeight), 2) AS Avg_Collection_Weight
                FROM Staff s
                JOIN LogStaff ls ON s.StaffID = ls.StaffID
                JOIN CollectionLog cl ON ls.CollectionLogID = cl.CollectionLogID
                GROUP BY s.StaffID, s.Name, s.Role
                ORDER BY Collections_Participated DESC
            """,
            
            6: """
                SELECT wt.Name AS Waste_Type,
                       COUNT(DISTINCT wb.BinID) AS Number_Of_Bins,
                       COUNT(DISTINCT wb.HouseholdID) AS Households_Using,
                       SUM(cd.CollectedWeight) AS Total_Weight_Collected,
                       wt.ProcessingCost AS Cost_Per_Unit,
                       ROUND(SUM(cd.CollectedWeight) * wt.ProcessingCost, 2) AS Total_Processing_Cost
                FROM WasteType wt
                LEFT JOIN WasteBin wb ON wt.WasteTypeID = wb.WasteTypeID
                LEFT JOIN CollectionDetails cd ON wb.BinID = cd.WasteBinID
                GROUP BY wt.WasteTypeID, wt.Name, wt.ProcessingCost
                ORDER BY Total_Weight_Collected DESC
            """,
            
            7: """
                SELECT r.RouteID,
                       r.Name AS Route_Name,
                       z.Name AS Zone_Name,
                       COUNT(DISTINCT h.HouseholdID) AS Total_Households,
                       COUNT(DISTINCT cs.ScheduleID) AS Scheduled_Collections,
                       COUNT(DISTINCT cl.CollectionLogID) AS Actual_Collections,
                       ROUND(AVG(cl.TotalRouteWeight), 2) AS Avg_Weight_Per_Collection
                FROM Route r
                JOIN Zone z ON r.ZoneID = z.ZoneID
                LEFT JOIN Household h ON r.RouteID = h.RouteID
                LEFT JOIN CollectionSchedule cs ON r.RouteID = cs.RouteID
                LEFT JOIN CollectionLog cl ON r.RouteID = cl.RouteID
                GROUP BY r.RouteID, r.Name, z.Name
                ORDER BY Total_Households DESC
            """,
            
            8: """
                SELECT h.Name AS Household_Name,
                       COUNT(p.PaymentID) AS Total_Payments,
                       SUM(CASE WHEN p.PaymentType = 'Service' THEN p.Amount ELSE 0 END) AS Service_Payments,
                       SUM(CASE WHEN p.PaymentType = 'Fine' THEN p.Amount ELSE 0 END) AS Fine_Payments,
                       SUM(p.Amount) AS Total_Amount_Paid
                FROM Household h
                LEFT JOIN Payment p ON h.HouseholdID = p.HouseholdID
                GROUP BY h.HouseholdID, h.Name
                ORDER BY Total_Amount_Paid DESC
            """,
            
            9: """
                SELECT rc.Name AS Center_Name,
                       rc.ProcessingCapacity AS Total_Capacity,
                       COUNT(DISTINCT cp.WasteTypeID) AS Waste_Types_Processed,
                       SUM(cp.ProcessingCapacity) AS Allocated_Capacity,
                       ROUND((rc.ProcessingCapacity - SUM(cp.ProcessingCapacity)), 2) AS Available_Capacity
                FROM RecyclingCenter rc
                LEFT JOIN CenterProcessing cp ON rc.CenterID = cp.CenterID
                GROUP BY rc.CenterID, rc.Name, rc.ProcessingCapacity
                ORDER BY Available_Capacity DESC
            """,
            
            10: """
                SELECT cs.CollectionDay,
                       COUNT(DISTINCT cs.ScheduleID) AS Scheduled_Collections,
                       COUNT(DISTINCT cl.CollectionLogID) AS Actual_Collections,
                       COUNT(DISTINCT cs.ScheduleID) - COUNT(DISTINCT cl.CollectionLogID) AS Missed_Collections,
                       ROUND(COUNT(DISTINCT cl.CollectionLogID) * 100.0 / 
                             NULLIF(COUNT(DISTINCT cs.ScheduleID), 0), 2) AS Compliance_Rate,
                       CASE 
                           WHEN COUNT(DISTINCT cl.CollectionLogID) * 100.0 / NULLIF(COUNT(DISTINCT cs.ScheduleID), 0) >= 95 THEN 'Excellent'
                           WHEN COUNT(DISTINCT cl.CollectionLogID) * 100.0 / NULLIF(COUNT(DISTINCT cs.ScheduleID), 0) >= 85 THEN 'Good'
                           WHEN COUNT(DISTINCT cl.CollectionLogID) * 100.0 / NULLIF(COUNT(DISTINCT cs.ScheduleID), 0) >= 70 THEN 'Fair'
                           ELSE 'Poor'
                       END AS Performance_Level
                FROM CollectionSchedule cs
                LEFT JOIN CollectionLog cl ON cs.RouteID = cl.RouteID
                    AND DATE(cl.CollectionDate) = cs.ScheduledDate
                GROUP BY cs.CollectionDay
                ORDER BY 
                    CASE cs.CollectionDay
                        WHEN 'Monday' THEN 1
                        WHEN 'Tuesday' THEN 2
                        WHEN 'Wednesday' THEN 3
                        WHEN 'Thursday' THEN 4
                        WHEN 'Friday' THEN 5
                        WHEN 'Saturday' THEN 6
                        WHEN 'Sunday' THEN 7
                    END
            """,
            
            11: """
                SELECT r.Name AS Route_Name,
                       z.Name AS Zone_Name,
                       COUNT(cl.CollectionLogID) AS Collection_Count,
                       SUM(cl.TotalRouteWeight) AS Total_Weight,
                       ROUND(AVG(cl.TotalRouteWeight), 2) AS Average_Weight
                FROM Route r
                JOIN Zone z ON r.ZoneID = z.ZoneID
                JOIN CollectionLog cl ON r.RouteID = cl.RouteID
                WHERE cl.CollectionDate >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                GROUP BY r.RouteID, r.Name, z.Name
                ORDER BY Total_Weight DESC
                LIMIT 5
            """,
            
            12: """
                SELECT DATE_FORMAT(v.DateIssued, '%Y-%m') AS Month,
                       COUNT(v.ViolationID) AS Total_Violations,
                       SUM(v.FineAmount) AS Total_Fines,
                       COUNT(DISTINCT v.HouseholdID) AS Households_With_Violations,
                       v.ViolationType
                FROM Violation v
                GROUP BY DATE_FORMAT(v.DateIssued, '%Y-%m'), v.ViolationType
                ORDER BY Month DESC, Total_Violations DESC
            """
        }

        if query_num in queries:
            try:
                conn = mysql.connector.connect(**self.db_config)
                cursor = conn.cursor()
                cursor.execute(queries[query_num])
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                
                converted_results = []
                for row in results:
                    converted_row = []
                    for val in row:
                        if isinstance(val, Decimal):
                            converted_row.append(float(val))
                        else:
                            converted_row.append(val)
                    converted_results.append(converted_row)

                self.last_results = pd.DataFrame(converted_results, columns=columns)

                self.display_results(columns, results)

                self.update_viz_button(query_num)

                cursor.close()
                conn.close()
                
            except mysql.connector.Error as err:
                self.result_text.insert(tk.END, f"Database Error: {err}\n")
                messagebox.showerror("Database Error", str(err))
        else:
            messagebox.showerror("Error", "Invalid query number")
    
    def update_viz_button(self, query_num):
        """Update the visualization button based on query type"""
        if self.viz_button:
            self.viz_button.destroy()

        viz_type, button_text, description = self.query_visualizations[query_num]

        colors = {
            'bar': '#2E86AB',
            'scatter': '#C73E1D',
            'boxplot': '#17A2B8',
            'pie': '#F18F01',
            'line': '#A23B72',
            'horizontal_bar': '#6A994E',
            'grouped_bar': '#006BA6',
            'heatmap': '#5D576B',
            'stacked_bar': '#4A5859',
            'area': '#8B5A3C'
        }
        
        self.viz_button = tk.Button(self.viz_button_frame, 
                                   text=button_text,
                                   command=lambda: self.show_visualization(viz_type),
                                   bg=colors.get(viz_type, '#2E86AB'),
                                   fg='white',
                                   font=('Arial', 10, 'bold'),
                                   width=18,
                                   relief=tk.RAISED,
                                   bd=2)
        self.viz_button.pack()

        self.status_label.config(text=f"✓ Query executed. Recommended: {description}", 
                                foreground='green')
    
    def display_results(self, columns, results):
        """Display query results in text area with proper formatting"""
        self.result_text.delete(1.0, tk.END)
        
        if not results:
            self.result_text.insert(tk.END, "No results found.")
            return

        from decimal import Decimal
        converted_results = []
        for row in results:
            converted_row = []
            for val in row:
                if isinstance(val, Decimal):
                    converted_row.append(float(val))
                else:
                    converted_row.append(val)
            converted_results.append(converted_row)

        col_widths = []
        for i, col in enumerate(columns):
            max_width = len(col)
            for row in converted_results:
                val_str = str(row[i]) if row[i] is not None else "NULL"
                if isinstance(row[i], float):
                    val_str = f"{row[i]:.2f}" if row[i] != int(row[i]) else str(int(row[i]))
                max_width = max(max_width, len(val_str))
            col_widths.append(min(max_width + 2, 30))

        header_parts = []
        for i, col in enumerate(columns):
            header_parts.append(f"{col:<{col_widths[i]}}")
        header = " | ".join(header_parts)
        self.result_text.insert(tk.END, "Query Results\n")
        self.result_text.insert(tk.END, header + "\n")
        self.result_text.insert(tk.END, "-" * len(header) + "\n")
        
        for row_idx, row in enumerate(converted_results):
            row_parts = []
            for i, val in enumerate(row):
                if val is None:
                    formatted_val = "NULL"
                elif isinstance(val, float):
                    formatted_val = f"{val:.2f}" if val != int(val) else str(int(val))
                else:
                    formatted_val = str(val)
                row_parts.append(f"{formatted_val:<{col_widths[i]}}")
            row_text = " | ".join(row_parts)
            self.result_text.insert(tk.END, f"{row_idx+1:<3} | {row_text}\n")
        
        self.result_text.insert(tk.END, f"\nTotal rows: {len(results)}\n")
    
    def show_visualization(self, viz_type):
        """Show appropriate visualization based on query type"""
        if self.last_results is None or self.last_query_type is None:
            messagebox.showinfo("Info", "Please execute a query first")
            return

        viz_window = tk.Toplevel(self.root)
        viz_window.title(f"Query {self.last_query_type} Visualization")
        viz_window.geometry("900x700")

        fig = plt.Figure(figsize=(12, 8), dpi=80)

        if viz_type == 'bar':
            self.create_bar_chart(fig)
        elif viz_type == 'scatter':
            self.create_scatter_plot(fig)
        elif viz_type == 'boxplot':
            self.create_boxplot(fig)
        elif viz_type == 'pie':
            self.create_pie_chart(fig)
        elif viz_type == 'horizontal_bar':
            self.create_horizontal_bar(fig)
        elif viz_type == 'grouped_bar':
            self.create_grouped_bar(fig)
        elif viz_type == 'heatmap':
            self.create_heatmap(fig)
        elif viz_type == 'stacked_bar':
            self.create_stacked_bar(fig)
        elif viz_type == 'line':
            self.create_line_chart(fig)
        elif viz_type == 'area':
            self.create_area_chart(fig)

        canvas = FigureCanvasTkAgg(fig, master=viz_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_bar_chart(self, fig):
        """Bar chart for queries 1, 11"""
        ax = fig.add_subplot(111)

        if self.last_query_type == 1:
            x_col = 'Zone_Name'
            y_col = 'Total_Weight_Collected'
            title = 'Waste Collection by Zone'
        else:
            x_col = 'Route_Name'
            y_col = 'Total_Weight'
            title = 'Top 5 Performing Routes'

        data = self.last_results
        bars = ax.bar(data[x_col], data[y_col], color='steelblue', edgecolor='navy', linewidth=1.5)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel(x_col.replace('_', ' '), fontsize=12)
        ax.set_ylabel(y_col.replace('_', ' '), fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        fig.tight_layout()
    
    def create_scatter_plot(self, fig):
        """Scatter plot for query 2 (Recycling rates)"""
        ax = fig.add_subplot(111)

        data = self.last_results.head(20)

        x = pd.to_numeric(data['Total_Bins'], errors='coerce').fillna(0)
        y = pd.to_numeric(data['Recycling_Rate_Percentage'], errors='coerce').fillna(0)

        if len(x) == 0 or len(y) == 0:
            ax.text(0.5, 0.5, 'No valid data for scatter plot', ha='center', va='center', 
                   transform=ax.transAxes, fontsize=14)
            ax.set_title('Recycling Rate Analysis - No Data', fontsize=16, fontweight='bold')
            fig.tight_layout()
            return

        colors = y
        scatter = ax.scatter(x, y, c=colors, cmap='RdYlGn', s=100, 
                           alpha=0.6, edgecolors='black', linewidth=1)

        from matplotlib import pyplot as plt
        cbar = fig.colorbar(scatter, ax=ax)
        cbar.set_label('Recycling Rate %', fontsize=10)

        try:
            if len(x) > 1 and x.std() > 0:
                z = np.polyfit(x.values, y.values, 1)
                p = np.poly1d(z)
                ax.plot(x, p(x), "r--", alpha=0.8, label='Trend line')
                ax.legend()
        except Exception as e:
            print(f"Could not add trend line: {e}")

        ax.set_title('Household Recycling Rate Analysis', fontsize=16, fontweight='bold')
        ax.set_xlabel('Total Bins', fontsize=12)
        ax.set_ylabel('Recycling Rate (%)', fontsize=12)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
    
    def create_boxplot(self, fig):
        """Box plot for Query 3 (Vehicle weight distribution)"""
        ax = fig.add_subplot(111)

        data = self.last_results

        vehicles = []
        weights = []

        for _, row in data.iterrows():
            if row['Total_Collections'] > 0:
                vehicles.append(f"{row['Model']} ({row['LicensePlate']})")
                weights.append(row['Avg_Weight_Per_Collection'])

        if weights:
            bp = ax.boxplot([weights], labels=['All Vehicles'], patch_artist=True)
            
            for patch in bp['boxes']:
                patch.set_facecolor('#17A2B8')
                patch.set_alpha(0.7)
            
            x = np.random.normal(1, 0.02, size=len(weights))
            ax.scatter(x, weights, alpha=0.6, s=50, color='red')
            
            for i, (xi, yi, label) in enumerate(zip(x, weights, vehicles)):
                if i < 5:
                    ax.annotate(label, (xi, yi), fontsize=8, 
                               xytext=(5, 5), textcoords='offset points')

        ax.set_ylabel('Average Weight Per Collection (kg)', fontsize=12)
        ax.set_title('Vehicle Weight Distribution Analysis', fontsize=16, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')

        if weights:
            mean_weight = np.mean(weights)
            median_weight = np.median(weights)
            ax.axhline(y=mean_weight, color='green', linestyle='--', alpha=0.7, label=f'Mean: {mean_weight:.1f}')
            ax.axhline(y=median_weight, color='orange', linestyle='--', alpha=0.7, label=f'Median: {median_weight:.1f}')
            ax.legend()
        
        fig.tight_layout()
    
    def create_horizontal_bar(self, fig):
        """Horizontal bar for query 4 (Violations)"""
        ax = fig.add_subplot(111)

        data = self.last_results.head(10)
        y_pos = np.arange(len(data))

        bars = ax.barh(y_pos, data['Outstanding_Fines'], color='crimson', alpha=0.7)

        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2., 
                   f'${width:.0f}', ha='left', va='center', fontsize=9)

        ax.set_yticks(y_pos)
        ax.set_yticklabels(data['Household_Name'])
        ax.set_xlabel('Outstanding Fines ($)', fontsize=12)
        ax.set_title('Top 10 Households with Outstanding Violations', fontsize=16, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        fig.tight_layout()
    
    def create_grouped_bar(self, fig):
        """Grouped bar chart for Query 5 (Staff) and Query 9 (Recycling centers)"""
        ax = fig.add_subplot(111)

        data = self.last_results

        if self.last_query_type == 5:
            data = data.head(10)

            if len(data) == 0:
                ax.text(0.5, 0.5, 'No staff data available', ha='center', va='center', 
                       transform=ax.transAxes, fontsize=14)
                ax.set_title('Staff Performance - No Data', fontsize=16, fontweight='bold')
                return
            
            x_pos = np.arange(len(data))
            width = 0.25

            collections = data['Collections_Participated'].fillna(0)
            routes = data['Routes_Covered'].fillna(0)
            avg_weight = data['Avg_Collection_Weight'].fillna(0)

            if avg_weight.max() > 0:
                avg_weight_scaled = (avg_weight / avg_weight.max()) * 10
            else:
                avg_weight_scaled = avg_weight

            bars1 = ax.bar(x_pos - width, collections, width, label='Collections', color='#2E86AB', alpha=0.8)
            bars2 = ax.bar(x_pos, routes, width, label='Routes', color='#F18F01', alpha=0.8)
            bars3 = ax.bar(x_pos + width, avg_weight_scaled, width, label='Avg Weight (scaled)', color='#6A994E', alpha=0.8)
            
            for bars in [bars1, bars2, bars3]:
                for bar in bars:
                    height = bar.get_height()
                    if height > 0:
                        ax.text(bar.get_x() + bar.get_width()/2., height,
                               f'{height:.1f}', ha='center', va='bottom', fontsize=8)
            
            ax.set_xlabel('Staff Members', fontsize=12)
            ax.set_ylabel('Count / Scale', fontsize=12)
            ax.set_title('Staff Performance Metrics - Top 10', fontsize=16, fontweight='bold')
            ax.set_xticks(x_pos)
            ax.set_xticklabels(data['Name'], rotation=45, ha='right')
            
        else:
            if len(data) == 0:
                ax.text(0.5, 0.5, 'No recycling center data available', ha='center', va='center', 
                       transform=ax.transAxes, fontsize=14)
                ax.set_title('Recycling Centers - No Data', fontsize=16, fontweight='bold')
                return
            
            x_pos = np.arange(len(data))
            width = 0.35

            total_capacity = data['Total_Capacity'] / 1000
            allocated = data['Allocated_Capacity'] / 1000
            available = data['Available_Capacity'] / 1000

            bars1 = ax.bar(x_pos - width/2, allocated, width, label='Allocated (×1000 kg)', 
                          color='#FF6B6B', alpha=0.8)
            bars2 = ax.bar(x_pos + width/2, available, width, label='Available (×1000 kg)', 
                          color='#4ECDC4', alpha=0.8)

            for bars in [bars1, bars2]:
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.1f}', ha='center', va='bottom', fontsize=9)
            
            ax.set_xlabel('Recycling Center', fontsize=12)
            ax.set_ylabel('Capacity (×1000 kg)', fontsize=12)
            ax.set_title('Recycling Center Capacity Analysis', fontsize=16, fontweight='bold')
            ax.set_xticks(x_pos)
            ax.set_xticklabels(data['Center_Name'], rotation=45, ha='right')
        
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3, axis='y')
        fig.tight_layout()
    
    def create_pie_chart(self, fig):
        """Pie chart for query 6 (Waste type distribution)"""
        ax = fig.add_subplot(111)
        
        data = self.last_results[self.last_results['Total_Weight_Collected'].notna()]
        values = data['Total_Weight_Collected']
        labels = data['Waste_Type']
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(values)))
        wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%',
                                          colors=colors, startangle=90,
                                          shadow=True, explode=[0.05]*len(values))
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        ax.set_title('Waste Type Distribution', fontsize=16, fontweight='bold')
        fig.tight_layout()
    
    def create_heatmap(self, fig):
        """Heatmap for query 7 (Route efficiency)"""
        ax = fig.add_subplot(111)
        
        try:
            if 'Zone_Name' not in self.last_results.columns or \
               'Route_Name' not in self.last_results.columns or \
               'Avg_Weight_Per_Collection' not in self.last_results.columns:
                self.create_route_efficiency_bar(fig, ax)
                return
            
            pivot_data = self.last_results.pivot_table(
                index='Zone_Name', 
                columns='Route_Name', 
                values='Avg_Weight_Per_Collection',
                fill_value=0
            )
            
            if pivot_data.empty or len(pivot_data) < 2:
                self.create_route_efficiency_bar(fig, ax)
                return
            
            im = ax.imshow(pivot_data, cmap='YlOrRd', aspect='auto')

            ax.set_xticks(np.arange(len(pivot_data.columns)))
            ax.set_yticks(np.arange(len(pivot_data.index)))
            ax.set_xticklabels(pivot_data.columns, rotation=45, ha='right')
            ax.set_yticklabels(pivot_data.index)

            cbar = fig.colorbar(im, ax=ax)
            cbar.set_label('Avg Weight per Collection', rotation=270, labelpad=15)

            for i in range(len(pivot_data.index)):
                for j in range(len(pivot_data.columns)):
                    if not np.isnan(pivot_data.iloc[i, j]):
                        text = ax.text(j, i, f'{pivot_data.iloc[i, j]:.0f}',
                                     ha="center", va="center", color="black", fontsize=9)
            
            ax.set_title('Route Efficiency Heatmap', fontsize=16, fontweight='bold')
            
        except Exception as e:
            self.create_route_efficiency_bar(fig, ax)
            
        fig.tight_layout()
    
    def create_route_efficiency_bar(self, fig, ax):
        """Fallback bar chart for route efficiency"""
        ax.clear()
        data = self.last_results.head(10)

        if len(data) > 0:
            x_pos = np.arange(len(data))
            bars = ax.bar(x_pos, data['Avg_Weight_Per_Collection'].fillna(0), 
                         color='#5D576B', alpha=0.7)

            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.1f}', ha='center', va='bottom', fontsize=9)
            
            ax.set_xticks(x_pos)
            ax.set_xticklabels(data['Route_Name'], rotation=45, ha='right')
            ax.set_ylabel('Avg Weight per Collection', fontsize=12)
            ax.set_title('Route Efficiency Analysis', fontsize=16, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
        else:
            ax.text(0.5, 0.5, 'No route data available', ha='center', va='center', 
                   transform=ax.transAxes, fontsize=14)
            ax.set_title('Route Efficiency - No Data', fontsize=16, fontweight='bold')
    
    def create_stacked_bar(self, fig):
        """Stacked bar for query 8 (Payments)"""
        ax = fig.add_subplot(111)

        data = self.last_results.head(10)
        x_pos = range(len(data))

        service = data['Service_Payments']
        fines = data['Fine_Payments']

        ax.bar(x_pos, service, label='Service Payments', color='#2E86AB', alpha=0.8)
        ax.bar(x_pos, fines, bottom=service, label='Fine Payments', color='#A23B72', alpha=0.8)

        ax.set_xticks(x_pos)
        ax.set_xticklabels(data['Household_Name'], rotation=45, ha='right')
        ax.set_ylabel('Amount ($)', fontsize=12)
        ax.set_title('Payment Analysis by Household', fontsize=16, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        fig.tight_layout()
    
    def create_line_chart(self, fig):
        """Line chart for Query 10 (Compliance trends)"""
        ax = fig.add_subplot(111)

        data = self.last_results

        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        data['CollectionDay'] = pd.Categorical(data['CollectionDay'], categories=days_order, ordered=True)
        data = data.sort_values('CollectionDay')

        ax.plot(data['CollectionDay'], data['Compliance_Rate'], 
               marker='o', linewidth=2, markersize=10, color='green', label='Compliance Rate')

        for x, y in zip(data['CollectionDay'], data['Compliance_Rate']):
            ax.annotate(f'{y:.1f}%', (x, y), textcoords="offset points",
                       xytext=(0,10), ha='center', fontsize=9)

        ax.axhline(y=100, color='r', linestyle='--', alpha=0.5, label='Target (100%)')
        ax.axhline(y=95, color='orange', linestyle='--', alpha=0.3, label='Excellent (95%)')
        ax.axhline(y=85, color='blue', linestyle='--', alpha=0.3, label='Good (85%)')
        
        ax.set_title('Collection Schedule Compliance by Day', fontsize=16, fontweight='bold')
        ax.set_xlabel('Day of Week', fontsize=12)
        ax.set_ylabel('Compliance Rate (%)', fontsize=12)
        ax.set_ylim([0, 110])
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
    
    def create_area_chart(self, fig):
        """Area chart for query 12 (Violation trends)"""
        ax = fig.add_subplot(111)

        grouped = self.last_results.groupby('Month').agg({
            'Total_Violations': 'sum',
            'Total_Fines': 'sum'
        }).reset_index()
        grouped = grouped.sort_values('Month')

        x = range(len(grouped))

        ax.fill_between(x, grouped['Total_Violations'], alpha=0.5, color='crimson', label='Violations')
        ax.plot(x, grouped['Total_Violations'], color='darkred', linewidth=2, marker='o')

        ax2 = ax.twinx()
        ax2.fill_between(x, grouped['Total_Fines'], alpha=0.3, color='orange', label='Fines')
        ax2.plot(x, grouped['Total_Fines'], color='darkorange', linewidth=2, marker='s')

        ax.set_xticks(x)
        ax.set_xticklabels(grouped['Month'], rotation=45, ha='right')
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('Total Violations', fontsize=12, color='darkred')
        ax2.set_ylabel('Total Fines ($)', fontsize=12, color='darkorange')
        
        ax.set_title('Violation Trends Over Time', fontsize=16, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        fig.tight_layout()

def main():
    root = tk.Tk()
    app = WasteManagementGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
