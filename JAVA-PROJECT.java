import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class HotelManagementGUI {
    private JFrame frame;
    private Connection conn;

    public HotelManagementGUI() throws SQLException {
        // Establish database connection
        String url = "jdbc:mysql://localhost:3306/hotel_management";
        String user = "root"; // Change as needed
        String password = "Hv279Chi"; // Change as needed
        conn = DriverManager.getConnection(url, user, password);

        // Set up the GUI frame
        frame = new JFrame("Hotel Management");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(490, 208);
        frame.setLayout(new FlowLayout());

        // Create buttons
        JButton addCustomerButton = new JButton("Add Customer");
        JButton checkRoomAvailabilityButton = new JButton("Check Room Availability");

        frame.add(addCustomerButton);
        frame.add(checkRoomAvailabilityButton);

        // Button actions
        addCustomerButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                showAddCustomerDialog();
            }
        });

        checkRoomAvailabilityButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                showCheckRoomAvailabilityDialog();
            }
        });

        frame.setVisible(true);
    }

    private void showAddCustomerDialog() {
        JDialog dialog = new JDialog(frame, "Add Customer");
        dialog.setSize(300, 150);
        dialog.setLayout(new FlowLayout());

        JLabel nameLabel = new JLabel("Name: ");
        JTextField nameField = new JTextField(20);
        JLabel roomLabel = new JLabel("Room Number: ");
        JTextField roomField = new JTextField(5);
        JButton addButton = new JButton("Add");

        addButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String name = nameField.getText();
                int roomNumber = Integer.parseInt(roomField.getText());

                try {
                    // Insert customer into database
                    String query = "INSERT INTO customers (name, room_number) VALUES (?, ?)";
                    PreparedStatement stmt = conn.prepareStatement(query);
                    stmt.setString(1, name);
                    stmt.setInt(2, roomNumber);
                    stmt.executeUpdate();

                    JOptionPane.showMessageDialog(dialog, "Customer added successfully!");
                } catch (SQLException ex) {
                    JOptionPane.showMessageDialog(dialog, "Error: " + ex.getMessage());
                }

                dialog.dispose();
            }
        });

        dialog.add(nameLabel);
        dialog.add(nameField);
        dialog.add(roomLabel);
        dialog.add(roomField);
        dialog.add(addButton);
        dialog.setVisible(true);
    }

    private void showCheckRoomAvailabilityDialog() {
        JDialog dialog = new JDialog(frame, "Check Room Availability");
        dialog.setSize(250, 150);
        dialog.setLayout(new FlowLayout());

        JLabel roomLabel = new JLabel("Room Number: ");
        JTextField roomField = new JTextField(5);
        JButton checkButton = new JButton("Check");

        checkButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                int roomNumber = Integer.parseInt(roomField.getText());

                try {
                    // Check room availability
                    String query = "SELECT is_occupied FROM rooms WHERE room_number = ?";
                    PreparedStatement stmt = conn.prepareStatement(query);
                    stmt.setInt(1, roomNumber);
                    ResultSet rs = stmt.executeQuery();

                    if (rs.next()) {
                        boolean isOccupied = rs.getBoolean("is_occupied");
                        String message = isOccupied ? "Room " + roomNumber + " is occupied." : "Room " + roomNumber + " is available.";
                        JOptionPane.showMessageDialog(dialog, message);
                    } else {
                        JOptionPane.showMessageDialog(dialog, "Room not found.");
                    }
                } catch (SQLException ex) {
                    JOptionPane.showMessageDialog(dialog, "Error: " + ex.getMessage());
                }

                dialog.dispose();
            }
        });

        dialog.add(roomLabel);
        dialog.add(roomField);
        dialog.add(checkButton);
        dialog.setVisible(true);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            try {
                new HotelManagementGUI();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        });
    }
}
