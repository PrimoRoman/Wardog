#!/Users/romi/miniconda3/envs/py312/bin/python3

######
# add primary and secondary VP
# add more buttons for primary and secondary vp
# victory_points = secondary_points + primary_points
# max vp for primary is 50
# max vp for secondary is 40
#
######
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QFileDialog, QMessageBox, QFrame
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
import sys
import csv
import time

#PRIMARY_COLORS = ["red", "blue", "green", "yellow", "black", "white"]

class Player: 
    def __init__(self, name):
        self.name = name
        self.time_elapsed = 0
        self.command_points = 0
        self.primary_points = 0
        self.secondary_points = 0
        self.painted = 0
        self.victory_points = 0
        self.turns = 0
        self.last_active = None
        self.color = "white"

class WarhammerClockApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Warhammer 40k Clock")
        self.resize(900, 600)
        self.setStyleSheet("background-color: #1e1e1e; color: #e0dede;")
        self.players = [Player("Player 1"), Player("Player 2")]
        self.active_player = None
        self.running = False
        self.battle_round = 1
        self.log = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.build_ui()

    def build_ui(self):
        main_layout = QVBoxLayout() # main body
        
        self.round_label = QLabel(f"Battle Round {self.battle_round} - Player 1's Turn") # upper label
        self.round_label.setFont(QFont("Times New Roman", 48, QFont.Weight.Bold)) # font
        self.round_label.setAlignment(Qt.AlignmentFlag.AlignCenter) # alignment 
        self.round_label.setStyleSheet("color: #d4af37;") # color of text: #d4af37 goldish yellow
        main_layout.addWidget(self.round_label) # submit label

        grid = QHBoxLayout()
        self.name_edits = []
        self.time_labels = []
        self.cp_labels = []
        self.vp_labels1 = []
        self.vp_labels2 = []
        self.vp_labels = [] # change to sum
        self.panels = []
        for i, player in enumerate(self.players): # for each player make a frame and populate it
            panel = QFrame() # panel refers to the rectangles in which the player time and points sit 
            panel.setFrameShape(QFrame.Shape.StyledPanel) # QFrame.Shape.StyledPanel 
            panel.setStyleSheet("QFrame { border: 2px solid #d4af37; border-radius: 10px; }") # panel style
            vbox = QVBoxLayout(panel) # vbox is the output of panel (generate QVBoxLayout?) 

            # name edit
            name_edit = QLineEdit(player.name) 
            name_edit.setFont(QFont("Arial", 24, QFont.Weight.Bold))
            name_edit.setStyleSheet("background-color: #2b2b2b; color: #e0dede;")
            vbox.addWidget(name_edit)
            self.name_edits.append((player, name_edit))

            # initialize clock
            time_lbl = QLabel("00:00")
            time_lbl.setFont(QFont("Arial", 186, QFont.Weight.Bold))
            time_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            vbox.addWidget(time_lbl, stretch=1)
            self.time_labels.append(time_lbl)

            # cp label
            label = QLabel("ComPts:")
            label.setFont(QFont("Menlo", 32))
            #label.setStyleSheet("font-size: 32pt;") # Increase to 18 points
            cp_h = QHBoxLayout()
            cp_h.addWidget(label)

            # cp number label
            cp_lbl = QLabel("0")
            cp_lbl.setFont(QFont("Menlo", 32))
            cp_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

            #cp_lbl.setStyleSheet("font-size: 32pt;")
            cp_h.addWidget(cp_lbl)
            self.cp_labels.append(cp_lbl)

            #add cp button
            btn_add_cp = QPushButton("+")
            btn_add_cp.setStyleSheet("""QPushButton {color: white;width: 32px;height: 37px;font-size: 32px;font-weight: bold;border: 2px solid #d4af37;border-radius:10px;}""")
            btn_add_cp.clicked.connect(lambda _, p=player: self.add_cp(p))
            cp_h.addWidget(btn_add_cp)

            #subtract cp button
            btn_sub_cp = QPushButton("-")
            btn_sub_cp.setStyleSheet("""QPushButton {color: white;width: 32px;height: 37px;font-size: 32px;font-weight: bold;border: 2px solid #d4af37;border-radius:10px;}""")
            btn_sub_cp.clicked.connect(lambda _, p=player: self.remove_cp(p))
            cp_h.addWidget(btn_sub_cp)
            vbox.addLayout(cp_h)

            # [primary:][number][+][-]
            pri_vp_h = QHBoxLayout() # add widget row
            
            # adding Primary:
            
            label = QLabel("PriPts:")
            label.setFont(QFont("Menlo", 32))
            label.setStyleSheet("font-size: 32pt;")
            pri_vp_h.addWidget(label)

            #adding number box that can be updated
            pri_vp_lbl = QLabel("0")
            pri_vp_lbl.setFont(QFont("Menlo", 32))
            pri_vp_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.vp_labels1.append(pri_vp_lbl)
            pri_vp_h.addWidget(pri_vp_lbl)

            pri_btn_add_vp = QPushButton("+") # plus button
            pri_btn_add_vp.setStyleSheet("""QPushButton {color: white;width: 32px;height: 37px;font-size: 32px;font-weight: bold;border: 2px solid #d4af37;border-radius:10px;}""")
            pri_btn_add_vp.clicked.connect(lambda _, p=player: self.add_primary_vp(p))
            pri_vp_h.addWidget(pri_btn_add_vp)

            pri_btn_sub_vp = QPushButton("-")
            pri_btn_sub_vp.setStyleSheet("""QPushButton {color: white;width: 32px;height: 37px;font-size: 32px;font-weight: bold;border: 2px solid #d4af37;border-radius:10px;}""")
            pri_btn_sub_vp.clicked.connect(lambda _, p=player: self.remove_primary_vp(p))
            pri_vp_h.addWidget(pri_btn_sub_vp)
            
            # submit widget row to vbox
            vbox.addLayout(pri_vp_h) # how to put in the row

            ## add secondary vp section ##

            # add widget row
            sec_vp_h = QHBoxLayout() 

            # add label
            label = QLabel("SecPts:")
            label.setFont(QFont("Menlo", 32))
            #label.setStyleSheet("font-size: 32pt;")
            sec_vp_h.addWidget(label)

            sec_vp_lbl = QLabel("0")
            sec_vp_lbl.setFont(QFont("Menlo",32))
            sec_vp_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            sec_vp_h.addWidget(sec_vp_lbl)
            self.vp_labels2.append(sec_vp_lbl)

            # add plus
            sec_btn_add_vp = QPushButton("+")
            sec_btn_add_vp.setStyleSheet("""QPushButton {color: white;width: 32px;height: 37px;font-size: 32px;font-weight: bold;border: 2px solid #d4af37;border-radius:10px;}""")
            sec_btn_add_vp.clicked.connect(lambda _, p=player: self.add_secondary_vp(p))
            sec_vp_h.addWidget(sec_btn_add_vp)

            sec_btn_sub_vp = QPushButton("-")
            sec_btn_sub_vp.setStyleSheet("""QPushButton {color: white;width: 32px;height: 37px;font-size: 32px;font-weight: bold;border: 2px solid #d4af37;border-radius:10px;}""")
            sec_btn_sub_vp.clicked.connect(lambda _, p=player: self.remove_secondary_vp(p))
            sec_vp_h.addWidget(sec_btn_sub_vp)



            vbox.addLayout(sec_vp_h) # how to put in the row
            ### fix sizing so it's not ugly?
            ### add plus 10 for painted army


            
            #VP label
            vp_h = QHBoxLayout() # this is the widget left to right position manager!!!!!! WOOOO
            label = QLabel("VicPts:") # Qlabel
            label.setFont(QFont("Menlo", 32))
            #label.setStyleSheet("font-size: 32pt;") # set font size
            vp_h.addWidget(label) # add to row left to right

            #VP number label
            vp_lbl = QLabel("0") # vp number label
            vp_lbl.setFont(QFont("Menlo", 32))
            vp_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

            vp_h.addWidget(vp_lbl)
            self.vp_labels.append(vp_lbl)

            #add VP button
            #btn_add_vp = QPushButton("+") # vp add
            #btn_add_vp.setStyleSheet("""QPushButton {color: white;width: 32px;height: 37px;font-size: 32px;font-weight: bold;border: 2px solid #d4af37;border-radius:10px;}""")
            #btn_add_vp.clicked.connect(lambda _, p=player: self.add_vp(p))
            #vp_h.addWidget(btn_add_vp)

            #subtract VP button
            #btn_sub_vp = QPushButton("-") # vp minus
            #btn_sub_vp.setStyleSheet("""QPushButton {color: white;width: 32px;height: 37px;font-size: 32px;font-weight: bold;border: 2px solid #d4af37;border-radius:10px;}""")
            #btn_sub_vp.clicked.connect(lambda _, p=player: self.remove_vp(p))
            #vp_h.addWidget(btn_sub_vp)
            
            vbox.addLayout(vp_h) # submit row

            #need to add another VP section with primary and secondary
            #maximum for primary and secondary is 50 and 40 respectively 

            
            ###  <-------------------------------------------- here is where i am
            ### add is painted bonus

            isPainted = QHBoxLayout() # is painted row
            
            label = QLabel("Painted?")
            label.setFont(QFont("Menlo", 32))
            isPainted.addWidget(label)

            yesno = QComboBox()
            yesno.addItems(['    no ','    Yes'])
            yesno.setFont(QFont("Menlo", 32))
            yesno.setStyleSheet("background-color: #2b2b2b; color: #e0dede;")
            yesno.currentIndexChanged.connect(lambda index, p=player,panel=panel: self.painted_points(p,panel,index))
            isPainted.addWidget(yesno)
            
            vbox.addLayout(isPainted)
            
            #end turn button
            btn_end = QPushButton("End Turn")
            btn_end.setStyleSheet("""QPushButton {width: 30px;height: 30px;background-color: #737373;font-size: 32px;font-weight: bold;border: 2px solid #d4af37;border-radius:10px;}""")
            btn_end.clicked.connect(lambda _, p=player: self.end_turn(p))
            vbox.addWidget(btn_end)

            #color_box ***remove this***
            #color_combo = QComboBox()
            #color_combo.addItems(PRIMARY_COLORS)
            #color_combo.setStyleSheet("background-color: #2b2b2b; color: #e0dede;")
            #color_combo.currentTextChanged.connect(lambda c, p=player, panel=panel: self.change_color(p, panel, c))
            #vbox.addWidget(color_combo)

            grid.addWidget(panel) #export panel
            self.panels.append(panel) #export panel

        main_layout.addLayout(grid)

        control_h = QHBoxLayout()
        buttons = [  #adding bottom buttons
            ("Start Game", self.start_game),
            ("Pause Game", self.pause_game),
            ("Resume Game", self.resume_game),
            ("End Game", self.end_game),
            ("Reset Game", self.reset_game),
            ("Export CSV", self.export_csv)
        ]
        for text, handler in buttons: # awesome, adds buttons in list of names with function
            btn = QPushButton(text)
            btn.clicked.connect(handler)
            btn.setFont(QFont("Arial", 24))
            btn.setFixedHeight(60)
            control_h.addWidget(btn)

        main_layout.addLayout(control_h)
        self.setLayout(main_layout)

    def reset_game(self):
        """Reset the entire game to initial state"""
        # Stop timer if running
        if self.timer.isActive():
            self.timer.stop()

        self.running = False
        self.active_player = None
        self.battle_round = 1
        self.log = []

        # Reset both players
        for player in self.players:
            player.time_elapsed = 0
            player.command_points = 0
            player.victory_points = 0
            player.primary_points = 0
            player.secondary_points = 0
            player.painted = 0
            player.turns = 0
            player.last_active = None

        # Reset round label
        self.round_label.setText(f"Battle Round {self.battle_round} - Player 1's Turn")

        # Update UI
        self.update_ui()

        QMessageBox.information(self, "Game Reset", "Game has been reset to initial state.")

    def start_game(self):
        if not self.active_player:
            self.active_player = self.players[0]
        self.active_player.last_active = time.time()
        self.running = True
        for p in self.players:
            p.command_points += 1
            p.turns = self.battle_round
        if not self.timer.isActive():
            self.timer.start(500)
        self.update_ui()

    def pause_game(self):
        if self.active_player and self.active_player.last_active is not None:
            now = time.time()
            elapsed = now - self.active_player.last_active
            self.active_player.time_elapsed += elapsed
            self.active_player.last_active = None
        self.running = False
        if self.timer.isActive():
            self.timer.stop()
        self.update_ui()

    def resume_game(self):
        if self.active_player and not self.running:
            self.active_player.last_active = time.time()
            self.running = True
            if not self.timer.isActive():
                self.timer.start(500)
        self.update_ui()

    def painted_points(self, player, panel, yes_or_no):
        if yes_or_no == 1:
            player.painted = 10
        if yes_or_no == 0:
            player.painted = 0
        
    def change_color(self, player, panel, color):
        player.color = color
        panel.setStyleSheet(f"QFrame {{ background-color: {color}; border: 2px solid #d4af37; border-radius: 10px; }}")

    def add_cp(self, player):
        player.command_points += 1
        self.update_points()

    def remove_cp(self, player):
        if player.command_points > 0:
            player.command_points -= 1
        self.update_points()

    def add_vp(self, player):
        
        player.victory_points += 1
        self.update_points()

    def add_primary_vp(self,player): # roman entered these manually
        if player.primary_points <50:
            player.primary_points += 1
        self.update_points()
    def remove_primary_vp(self,player): # roman entered these manually ### not working
        if player.primary_points > 0:
            player.primary_points -= 1
        self.update_points()

    def add_secondary_vp(self,player): # roman entered these manually
        if player.secondary_points < 40:
            player.secondary_points += 1
        self.update_points()
    def remove_secondary_vp(self,player): # roman entered these manually ### not working
        if player.secondary_points > 0:
            player.secondary_points -= 1
        self.update_points()

    def remove_vp(self, player):
        if player.victory_points > 0:
            player.victory_points -= 1
        self.update_points()

    def end_turn(self, player):
        if player == self.active_player:                
            now = time.time()
            elapsed = 0
            if self.active_player and self.active_player.last_active is not None:
                elapsed = now - self.active_player.last_active
                self.active_player.time_elapsed += elapsed
            prev_total = 0
            for entry in reversed(self.log):
                if entry.get("Player") == player.name:
                    prev_total = entry.get("VP total", 0)
                    break
            vp_delta = player.victory_points - prev_total
            turn_time = round(elapsed)
            self.log.append({
                "Round": self.battle_round,
                "Player": player.name,
                "VP total": player.victory_points,
                "VP delta": vp_delta,
                "CP": player.command_points,
                "Turn": player.turns,
                "Turn Time(s)": turn_time,
                "Turn Time": time.strftime("%H:%M:%S", time.gmtime(turn_time))
            })
            self.active_player = self.players[1] if player == self.players[0] else self.players[0]
            for p in self.players:
                p.command_points += 1
            self.active_player.last_active = now
            if self.active_player == self.players[0]:
                self.battle_round += 1
            self.round_label.setText(f"Battle Round {self.battle_round} - {self.active_player.name}'s Turn")
            self.active_player.turns = self.battle_round
            for p, name_edit in self.name_edits:
                p.name = name_edit.text()
            self.update_ui()

    def update_clock(self):
        if self.active_player and self.active_player.last_active is not None and self.running:
            now = time.time()
            elapsed = now - self.active_player.last_active
            total = self.active_player.time_elapsed + elapsed
            self.set_time_label(self.active_player, total)

    def set_time_label(self, player, total_seconds):
        mins, secs = divmod(int(total_seconds), 60)
        time_str = f"{mins:02d}:{secs:02d}"
        idx = self.players.index(player)
        self.time_labels[idx].setText(time_str)

    def update_ui(self):
        for i, player in enumerate(self.players):
            mins, secs = divmod(int(player.time_elapsed), 60)
            self.time_labels[i].setText(f"{mins:02d}:{secs:02d}") 
            self.cp_labels[i].setText(str(player.command_points))
            self.vp_labels1[i].setText(str(player.primary_points))
            self.vp_labels2[i].setText(str(player.secondary_points))
            self.vp_labels[i].setText(str(int(player.primary_points)+int(player.secondary_points)))
            player.victory_points = int(player.primary_points)+int(player.secondary_points)
            for p, name_edit in self.name_edits:
                p.name = name_edit.text()
                
    def update_points(self): # now the buttons don't show original time! AWESOME
        for i, player in enumerate(self.players):
            self.cp_labels[i].setText(str(player.command_points))
            self.vp_labels1[i].setText(str(player.primary_points))
            self.vp_labels2[i].setText(str(player.secondary_points))
            self.vp_labels[i].setText(str(int(player.primary_points)+int(player.secondary_points)))
            for p, name_edit in self.name_edits:
                p.name = name_edit.text()

    def update_ui_end(self):
        for i, player in enumerate(self.players):
            mins, secs = divmod(int(player.time_elapsed), 60)
            self.time_labels[i].setText(f"{mins:02d}:{secs:02d}") 
            self.cp_labels[i].setText(str(player.command_points))
            self.vp_labels1[i].setText(str(player.primary_points))
            self.vp_labels2[i].setText(str(player.secondary_points))
            
            self.vp_labels[i].setText(str(int(player.primary_points)+int(player.secondary_points)+int(player.painted)))            
            for p, name_edit in self.name_edits:
                p.name = name_edit.text()

    def export_csv(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if filename:
            with open(filename, "w", newline="") as f:
                fieldnames = ["Round", "Player", "VP total", "VP delta", "CP", "Turn", "Turn Time(s)", "Turn Time"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for entry in self.log:
                    writer.writerow(entry)
                f.write("\n")
                for player in self.players:
                    total_hms = time.strftime("%H:%M:%S", time.gmtime(player.time_elapsed))
                    writer.writerow({
                        "Round": "Summary",
                        "Player": player.name,
                        "VP total": player.victory_points,
                        "VP delta": "",
                        "CP": player.command_points,
                        "Turn": player.turns,
                        "Turn Time(s)": round(player.time_elapsed),
                        "Turn Time": total_hms
                    })

    def end_game(self):
        self.pause_game()
        self.update_ui_end()
        p1, p2 = self.players
        p1.victory_points = int(p1.primary_points)+int(p1.secondary_points)+int(p1.painted)
        p2.victory_points = int(p2.primary_points)+int(p2.secondary_points)+int(p2.painted)

        if p1.victory_points > p2.victory_points:
            winner, loser = p1, p2
        elif p2.victory_points > p1.victory_points:
            winner, loser = p2, p1
        else:
            winner, loser = None, None
        if winner:
            msg = f"{winner.name} WINS! {winner.victory_points} VP to {loser.victory_points} VP"
        else:
            msg = f"Game is a TIE! {p1.victory_points} VP to {p2.victory_points} VP"
        total_game_time = sum(p.time_elapsed for p in self.players)
        total_hms = time.strftime("%H:%M:%S", time.gmtime(total_game_time))
        end_game_msg_box = QMessageBox(self)
        end_game_msg_box.setText("Game Over!\n" + msg + f"\nTotal Game Time: {total_hms}")
        end_game_msg_box.setFont(QFont("Menlo", 32))
        end_game_msg_box.setMinimumWidth(600)
        #QMessageBox.information(self, "Game Over", msg + f"\nTotal Game Time: {total_hms}")
        end_game_msg_box.exec()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WarhammerClockApp()
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec())
