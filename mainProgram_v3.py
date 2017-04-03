import wx;
import serial;
import time;
import sys;
import math;

print "Initializing...";

global infoPanelWidth;
infoPanelWidth = 200;

global textOffset;
textOffset = 100;


class Mic(object):
    def __init__(self, label, wing, x, y, port):
        self.label = label;
        self.wing = wing;
        self.x = x;
        self.y = y;
        self.port = port;
        self.angle = 0;

class Map(object):

    micList = [];
    micStrings = []

    def __init__(self, name, height, width):
        self.name = name;
        self.height = height;
        self.width = width;

    def AddMic (self, unit):
        if not unit in self.micList:
            self.micList.append(unit);
        else:
            print ("Mic already placed.");

    def RemoveMic (self, unit):
        if not unit in self.micList:
            print ("Mic not in the set.");
        else:
            self.micList.remove(unit);

    def MicQuantity(self):
        return len(self.micList);

    def ShowMicStrings(self):
        for mic in self.micList:
            text = mic.label + ": (" + str(mic.x) + "," + str(mic.y) + ")";
            self.micStrings.append(text);
        return self.micStrings;


global stadium;
stadium = Map("Maracana", 100, 200);

global centerMic;
centerMic = Mic ("Z1", "North", 0, 0, 0);
stadium.AddMic(centerMic);

global northMic;
northMic = Mic ("N1", "North", 0, 314, 1);
stadium.AddMic(northMic);

global eastMic;
eastMic = Mic ("E1", "East", 516, 0, 2);
stadium.AddMic(eastMic);

global southMic;
southMic = Mic ("S1", "South", 0, -325, 3);
stadium.AddMic(southMic);

global westMic;
westMic = Mic ("W1", "West", -516, 0, 4);
stadium.AddMic(westMic);



class MainWindow (wx.Frame):
    #make sure it initializes
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs);

        self.SetBackgroundColour('#E1F5FE');
        #self.SetSize((1024, 768));
        self.SetTitle("Audio Tracker");
        self.Centre();
        self.Style = wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER;
        self.Show(True);

        self.BasicGUI();

    def BasicGUI(self):

        self.menuBar = wx.MenuBar();

        self.mainPanel = wx.Panel(self);

        self.vbox = wx.BoxSizer(wx.HORIZONTAL);


        fileMenu = wx.Menu();
        editMenu = wx.Menu();
        helpMenu = wx.Menu();
        microcontrollerMenu = wx.Menu();

        self.Bind (wx.EVT_CLOSE, self.Quit);

#### FileMenu Items
        newMapItem = fileMenu.Append(wx.ID_NEW, '&New Map\tCtrl+N', 'Create a new microphone mapping.');
        self.Bind(wx.EVT_MENU, self.CreateNewMap, newMapItem);

        openMapItem = fileMenu.Append(wx.ID_OPEN, '&Open Map\tCtrl+O', 'Open a previous built map.');
        self.Bind(wx.EVT_MENU, self.OpenMap, openMapItem);

        saveMapItem = fileMenu.Append(wx.ID_SAVE, '&Save Map\tCtrl+S', 'Save current map.');
        self.Bind(wx.EVT_MENU, self.SaveMap, saveMapItem);

        fileMenu.AppendSeparator();

        quitItem = fileMenu.Append(wx.ID_EXIT, '&Quit\tCtrl+W', 'Quit the Program.');
        self.Bind(wx.EVT_MENU, self.Quit, quitItem);

#### Edit Menu Items

        configureMapItem = editMenu.Append(wx.ID_ANY, 'Configure Mics Positions', 'Configure Microphones Location and Field Size.');
        self.Bind(wx.EVT_MENU, self.ConfigureMics, configureMapItem);

        editMenu.AppendSeparator();

        addMicItem = editMenu.Append(wx.ID_ANY, 'Add Mic', 'Add new Mic to the map.');
        self.Bind(wx.EVT_MENU, self.AddMic, addMicItem);

        removeMicItem = editMenu.Append(wx.ID_ANY, 'Remove Mic', 'Remove Mic from the map.');
        self.Bind(wx.EVT_MENU, self.RemoveMic, removeMicItem);

        calibrateLayoutItem = editMenu.Append(wx.ID_ANY, 'Calibrate Layout', 'Calibrate Layout Panel.');
        self.Bind(wx.EVT_MENU, self.CalibrateLayout, calibrateLayoutItem);

        editMenu.AppendSeparator();

        testMicRotationItem = editMenu.Append(wx.ID_ANY, 'Test Mics Rotation', 'Test Mics Rotation');
        self.Bind(wx.EVT_MENU, self.TestMicRotation, testMicRotationItem);

#### Microcontroller Menu Itens

        arduinoSubmenu = wx.Menu();

        initializeArduinoItem = arduinoSubmenu.Append(wx.ID_ANY, 'Initialize Arduino IDE', 'Initialize Arduino IDE');

        checkPortsItem = arduinoSubmenu.Append(wx.ID_ANY, 'Check Ports');
        self.Bind(wx.EVT_MENU, self.CheckPorts, checkPortsItem);

        microcontrollerMenu.AppendMenu(wx.ID_ANY, 'Arduino', arduinoSubmenu);

        raspberrySubmenu = wx.Menu();
        raspberrySubmenu.Append(wx.ID_ANY, 'Initialize Raspberry IDE', 'Initialize Arduino IDE');
        raspberrySubmenu.Append(wx.ID_ANY, 'Check Ports');

        microcontrollerMenu.AppendMenu(wx.ID_ANY, 'Raspberry', raspberrySubmenu);

        self.menuBar.Append(fileMenu, '&File');
        self.menuBar.Append(editMenu, '&Edit');
        self.menuBar.Append(microcontrollerMenu, '&Microcontroller');
        self.menuBar.Append(helpMenu, '&Help');

#### Help Menu Items

#Toolbar Functions
        toolbar = self.CreateToolBar();

        addMicToolbarItem = toolbar.AddLabelTool(wx.ID_ANY, 'Add', wx.Bitmap('addButton.png'));
        self.Bind(wx.EVT_TOOL, self.AddMic, addMicToolbarItem);

        removeMicToolbarItem = toolbar.AddLabelTool(wx.ID_ANY, 'Remove', wx.Bitmap('removeButton.png'));
        self.Bind(wx.EVT_TOOL, self.RemoveMic, removeMicToolbarItem);

        testMicRotationToolbarItem = toolbar.AddLabelTool(wx.ID_ANY, 'Test Mic Rotation', wx.Bitmap('rotateButton.png'));
        self.Bind(wx.EVT_TOOL, self.TestMicRotation, testMicRotationToolbarItem);

        calibrateLayoutToolbarItem = toolbar.AddLabelTool(wx.ID_ANY, 'Calibrate', wx.Bitmap('calibrateButton.png'));
        self.Bind(wx.EVT_TOOL, self.CalibrateLayout, calibrateLayoutToolbarItem);

        toolbar.Realize();

#### Color Properties
        self.midPanColour = '#424242';
        self.fieldPanelColour = '#424242';
        self.infoPanelColour = '#212121';
        self.infoPanelForegroundColour = "#FFFFFF"

#### Mid Pan Properties
        #global midPan;
        self.midPan = wx.Panel(self.mainPanel);
        self.midPan.SetBackgroundColour(self.midPanColour);

        self.vbox.Add(self.midPan, -1, wx.EXPAND | wx.ALL, 0);
        self.mainPanel.SetSizer(self.vbox);

        self.imageField = wx.Image("CampoFutebol4.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap();
        imageFieldOffset = 50;
        self.SetSize((self.imageField.GetWidth(),self.imageField.GetHeight()));
        #(self, parent, id=-1, pos=DefaultPosition, size=DefaultSize, style=wxTAB_TRAVERSAL|wxNO_BORDER, name=PanelNameStr)

#### Field Panel Properties

        self.fieldPanel = wx.Panel(self.midPan,
            pos=(10+infoPanelWidth,0),
            size = (75+imageFieldOffset+int(self.imageField.GetWidth()),self.imageField.GetHeight()+2*imageFieldOffset),
            style = wx.TRANSPARENT_WINDOW);

        self.fieldPanel.SetBackgroundColour(self.fieldPanelColour);

        self.button = wx.BitmapButton (self.fieldPanel, -1, self.imageField, pos = (imageFieldOffset, 5+imageFieldOffset/2));

        #wx.StaticBitmap(self.fieldPanel, -1, self.imageField, pos = (imageFieldOffset/2, imageFieldOffset/2), size = (self.imageField.GetWidth(), self.imageField.GetHeight()));

        #imageBall = wx.Image("exit.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap();
        #wx.StaticBitmap(self.button, -1, imageBall, pos = (cursorImageX, cursorImageY));

        self.button.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown);

#### Info Panel Properties
        #global infoPanel;
        self.infoPanel = wx.Panel (self.midPan, pos=(0,0), size=(infoPanelWidth,self.imageField.GetHeight()+2*imageFieldOffset));
        self.infoPanel.SetBackgroundColour(self.infoPanelColour);
        self.infoPanel.SetBackgroundColour(self.infoPanelColour);
        self.infoPanel.SetForegroundColour(self.infoPanelForegroundColour);

        self.infoPanel.Refresh();

        stadiumNameST = wx.StaticText(self.infoPanel, wx.ID_ANY, pos = (20,10), label = stadium.name, style=wx.ALIGN_LEFT);
        stadiumNameST.SetForegroundColour('#2196F3');

        self.cursorStaticText = wx.StaticText(self.infoPanel, wx.ID_ANY, pos = (20,100), label = '', style=wx.ALIGN_LEFT);

        self.ShowMicsPanel();

#### Status Bar
        status = self.CreateStatusBar();
        self.SetMenuBar(self.menuBar);


#### Functions

    def OnLeftDown(self,e):
        print ("\nLeft Mouse Button Pressed");
        x, y = e.GetPosition();
        cursorImageX = x-int(self.imageField.GetWidth())/2;
        cursorImageY = -y+int(self.imageField.GetHeight())/2;
        infoPanelText = "Cursor: ("+str(cursorImageX)+","+str(cursorImageY)+")";
        print infoPanelText;

        for mic in stadium.micList:
            #(xTarget, yTarget, wing, xMic, yMic);
            mic.angle = int(self.GetMicAngle(cursorImageX, cursorImageY, mic.wing, mic.x, mic.y));

        self.cursorStaticText.SetLabel(infoPanelText);
        self.ShowMicsPanel();
        self.SendTextToPort();

    def OpenMap(self,e):
        print ("Opening Previous Map");

    def SaveMap(self,e):
        print ("Saving Current Map");
        filename = (stadium.name).upper() + ".txt";
        f = open(filename,'w');
        if not (f.closed):
            print ("File " + filename + " opened for writing.");

        f.write(stadium.name+'\n');
        f.write(str(stadium.height)+'\n');
        f.write(str(stadium.width)+'\n');
        f.write(str(stadium.MicQuantity())+'\n');

        f.close();
        if (f.closed):
            print ("File " + filename + " closed.");

        print ("Current Map Saved.")

    def Quit(self, e):
        box = wx.MessageDialog(None, 'Are you sure you want to leave?', 'Quit', wx.YES_NO | wx.YES_DEFAULT);
        answer = box.ShowModal(); #returns the value of the Yes or No answer

        if (answer == wx.ID_YES):
            self.Destroy();

    def ConfigureMics(self,e):
        print ("Configuring Mics Position and Field Size");

    def AddMic(self,e):

        print ("Adding Mic to the Layout");

        additionWindow = AddMicWindow(None, -1);
        additionWindow.Show();

        print "Mic Added Succesfully"
        print "Stadium.MicQuantity(): " + str(stadium.MicQuantity());

        self.ShowMicsPanel();

    def RemoveMic(self,e):

        if (stadium.MicQuantity() == 0):
            box = wx.MessageDialog(None, 'There are no mics to be removed.', 'Zero mics', wx.OK);
            answer = box.ShowModal(); #returns the value of the Yes or No answer
            box.Destroy();

        else:
            print ("Removing Mic from the Layout");
            removalWindow = RemoveMicWindow(None, -1);
            removalWindow.Show();
            print "Stadium.MicQuantity(): " + str(stadium.MicQuantity());


        self.ShowMicsPanel();

    def GetSerialPort(self):
        #portas
        serialPorts = ['/dev/ttyACM0','/dev/ttyACM1','/dev/ttyACM2','/dev/ttyACM3'];

        for port in serialPorts:
            try:
                # Iniciando conexao serial
                comport = serial.Serial(port, 9600, timeout = 1);
                #time.sleep(1.8); # Entre 1.5s a 2s
                if (comport.isOpen() == True):
                    print "Port to be used: " + port;
                    comport.flush();
                    comport.close();
                    return port;
            except:
                pass;

        return "0";

    def CheckPorts(self,event):
        port = self.GetSerialPort();
        if (port == "0"):
            box = wx.MessageDialog(None, 'There are no microcontrollers connected.', 'Zero connections', wx.OK);
            answer = box.ShowModal(); #returns the value of the Yes or No answer
            box.Destroy();
        else:
            text = 'Connected port: ' + port;
            box = wx.MessageDialog(None, text, 'Connected Port', wx.OK);
            answer = box.ShowModal(); #returns the value of the Yes or No answer
            box.Destroy();

    def SendTextToPort(self):
        text = "Q" + str(stadium.MicQuantity())+":";
        count = 0;
        for mic in stadium.micList:
            text += mic.label+'['+str(mic.angle)+']';
            if (count < len(stadium.micList) - 1):

                text += ',';
            count += 1;
        text = text+".";
        print text;

        port = self.GetSerialPort();

        if (port == "0"):
            print "No microcontrollers connected"

        else:
            comport = serial.Serial(port, 9600, timeout = 1);
            comport.flush();

            # Time entre a conexao serial e o tempo para escrever (enviar algo)
            time.sleep(1.8) # Entre 1.5s a 2s

            for i in range (len(text)):
                comport.write(text[i].encode());
            #comport.write(PARAM_ASCII)

            VALUE_SERIAL=comport.readline()

            print '\nRetorno da serial: %s' % (VALUE_SERIAL)

            # Fechando conexao serial
            comport.close()



    def ShowMicsPanel(self):
        choicesList = [];
        for mic in stadium.micList:
            text = mic.label + ": (" + str(mic.x) + "," + str(mic.y) + ") @ " + str(mic.angle) + " dg";
            choicesList.append(text);
        dropDownMics = wx.ComboBox(self.infoPanel, -1, pos = (10,40), choices = choicesList);
        dropDownMics.SetValue("Mics");
        dropDownMics.SetSize((infoPanelWidth-30,30));
        dropDownMics.Update();

    def CalibrateLayout(self,e):
        print ("Calibrating Layout");
        self.ShowMicsPanel();
        print stadium.MicQuantity();

    def TestMicRotation(self,event):
        print ("Testing Rotation");
        rotationAngle = 0;
        while (rotationAngle <= 180):
            for mic in stadium.micList:
                mic.angle = rotationAngle;
            self.SendTextToPort();
            print ("Testing rotation angle: " + str(rotationAngle));
            rotationAngle += 45;
        print ("End of rotation test.");

    def CreateNewMap(self,e):
        print ("Creating New Map");
        creationWindow = NewMapWindow(None, 1);
        creationWindow.Show();

    def GetMicAngle (self, xTarget, yTarget, wing, xMic, yMic):

        if (wing.upper() == "SOUTH"):
            if (xTarget == xMic):
                return 90;
            elif (xTarget > xMic):
                return math.fabs(math.degrees(math.atan((yTarget-yMic)/(xTarget-xMic))));
            else:
                return 180-math.fabs(math.degrees(math.atan((yTarget-yMic)/(xTarget-xMic))));


        elif (wing.upper() == "NORTH"):
            if (xTarget == xMic):
                return 90;
            elif (xTarget > xMic):
                return 180-math.fabs(math.degrees(math.atan((yTarget-yMic)/(xTarget-xMic))));
            else:
                return math.fabs(math.degrees(math.atan((yTarget-yMic)/(xTarget-xMic))));

        elif (wing.upper() == "EAST"):
            if (yTarget == yMic):
                return 90;
            angle = 180-self.GetMicAngle (yTarget, xTarget, "North", yMic, xMic);
            return angle;


        elif (wing.upper() == "WEST"):
            if (yTarget == yMic):
                return 90;
            angle = self.GetMicAngle (yTarget, xTarget, "North", yMic, xMic);
            return angle;

        else:
            return "Error";



class NewMapWindow (wx.Frame):
    def __init__(self, *args, **kwargs):
        super(NewMapWindow, self).__init__(*args, **kwargs);
        self.SetSize((400, 300));
        self.SetTitle("Create New Map");
        self.Centre();
        self.Show(True);
        status = self.CreateStatusBar();
        self.BasicGUI();

    def BasicGUI(self):

        creationPanel = wx.Panel(self);

        verticalBox = wx.BoxSizer(wx.VERTICAL);

        layoutNameBox = wx.BoxSizer (wx.HORIZONTAL);
        layoutStaticText = wx.StaticText (creationPanel, label = "Layout Name : ");
        layoutNameBox.Add (layoutStaticText, flag = wx.RIGHT, border = 8);

        self.layoutTextControl = wx.TextCtrl (creationPanel);
        layoutNameBox.Add(self.layoutTextControl, proportion = 1);
        verticalBox.Add (layoutNameBox, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border = 10);

        verticalBox.Add((-1,5));


        layoutHeightBox = wx.BoxSizer (wx.HORIZONTAL);
        layoutHeightStaticText = wx.StaticText (creationPanel, label = "Height (meters): ");
        layoutHeightBox.Add (layoutHeightStaticText, flag = wx.RIGHT, border = 8);

        self.layoutHeightTextControl = wx.TextCtrl (creationPanel);
        layoutHeightBox.Add(self.layoutHeightTextControl, proportion = 1);
        verticalBox.Add (layoutHeightBox, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border = 10);

        verticalBox.Add((-1,5));


        layoutWidthBox = wx.BoxSizer (wx.HORIZONTAL);
        layoutWidthStaticText = wx.StaticText (creationPanel, label = "Width (meters): ");
        layoutWidthBox.Add (layoutWidthStaticText, flag = wx.RIGHT, border = 8);

        self.layoutWidthTextControl = wx.TextCtrl (creationPanel);
        layoutWidthBox.Add(self.layoutWidthTextControl, proportion = 1);
        verticalBox.Add (layoutWidthBox, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border = 10);

        verticalBox.Add((-1,5));


        verticalBox.Add((-1,20));

        micPropTextBox = wx.BoxSizer (wx.HORIZONTAL);
        micPropStaticText = wx.StaticText (creationPanel, label = "Mic Properties");
        micPropTextBox.Add (micPropStaticText, flag = wx.CENTER, border = 8);
        verticalBox.Add (micPropTextBox, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border = 10);

        verticalBox.Add((-1,10));


        micNumberBox = wx.BoxSizer (wx.HORIZONTAL);
        micNumberStaticText = wx.StaticText (creationPanel, label = "Number of Microphones : ");
        micNumberBox.Add (micNumberStaticText, flag = wx.RIGHT, border = 8);

        self.micNumberSpinCtrl = wx.SpinCtrl (creationPanel, -1, "", (150, 50));
        self.micNumberSpinCtrl.SetRange(1,20);
        self.micNumberSpinCtrl.SetValue (1);
        micNumberBox.Add(self.micNumberSpinCtrl, proportion = 1);
        verticalBox.Add (micNumberBox, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border = 10);


        verticalBox.Add((-1,10));

        buttonsBox= wx.BoxSizer (wx.HORIZONTAL);

        nextButton = wx.Button(creationPanel, label = "Next");
        buttonsBox.Add (nextButton, flag = wx.LEFT, border = 8);

        cancelButton = wx.Button (creationPanel, label = "Cancel");
        buttonsBox.Add (cancelButton, flag = wx.LEFT, border = 8);

        verticalBox.Add (buttonsBox, flag = wx.BOTTOM | wx.ALIGN_RIGHT, border = 10);

        verticalBox.Add((-1,10));

        creationPanel.SetSizer(verticalBox);

        self.Bind (wx.EVT_BUTTON, self.NextWindow, nextButton);
        self.Bind (wx.EVT_BUTTON, self.CloseWindow, cancelButton);

    def NextWindow (self,event):
        print "Next Window";
        print self.layoutTextControl.GetValue();
        print self.layoutHeightTextControl.GetValue();
        print self.layoutWidthTextControl.GetValue();
        print self.micNumberSpinCtrl.GetValue();

        self.Close(True);


    def CloseWindow(self, event):
        self.Close(True);

class AddMicWindow (wx.Frame):
    def __init__(self, *args, **kwargs):
        super(AddMicWindow, self).__init__(*args, **kwargs);
        self.SetSize((400, 340));
        self.SetTitle("Add New Mic");
        self.Centre();
        self.Show(True);
        status = self.CreateStatusBar();
        self.BasicGUI();

    def BasicGUI(self):

        creationPanel = wx.Panel(self);

        verticalBox = wx.BoxSizer(wx.VERTICAL);

        micPropTextBox = wx.BoxSizer (wx.HORIZONTAL);
        micPropStaticText = wx.StaticText (creationPanel, label = "Mic Properties");
        micPropTextBox.Add (micPropStaticText, flag = wx.CENTER, border = 8);
        verticalBox.Add (micPropTextBox, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border = 10);


        verticalBox.Add((-1,10));


        labelBox = wx.BoxSizer (wx.HORIZONTAL);
        labelStaticText = wx.StaticText (creationPanel, label = "Mic Label: ");
        labelBox.Add (labelStaticText, flag = wx.RIGHT, border = 8);

        self.labelTextControl = wx.TextCtrl (creationPanel);
        labelBox.Add(self.labelTextControl, proportion = 1);
        verticalBox.Add (labelBox, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border = 10);

        verticalBox.Add((-1,5));


        micWingBox = wx.BoxSizer (wx.HORIZONTAL);
        micWingStaticText = wx.StaticText (creationPanel, label = "Mic Wing: ");
        micWingBox.Add (micWingStaticText, flag = wx.RIGHT, border = 8);

        wingsList = ['East', 'North', 'South', 'West'];
        self.container = wx.ListBox (creationPanel, -1, (20,20), (80,95), wingsList, wx.LB_SINGLE);
        self.container.SetSelection(0); #default selection
        micWingBox.Add (self.container, proportion = 1);
        verticalBox.Add (micWingBox, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border = 10);

        verticalBox.Add((-1,10));

        micCoordinateXBox = wx.BoxSizer (wx.HORIZONTAL);
        micCoordinateXStaticText = wx.StaticText (creationPanel, label = "Coordinate X(meters): ");
        micCoordinateXBox.Add (micCoordinateXStaticText, flag = wx.RIGHT, border = 8);

        self.micCoordinateXTextControl = wx.TextCtrl (creationPanel);
        micCoordinateXBox.Add(self.micCoordinateXTextControl, proportion = 1);
        verticalBox.Add (micCoordinateXBox, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border = 10);

        verticalBox.Add((-1,5));

        micCoordinateYBox = wx.BoxSizer (wx.HORIZONTAL);
        micCoordinateYStaticText = wx.StaticText (creationPanel, label = "Coordinate Y(meters): ");
        micCoordinateYBox.Add (micCoordinateYStaticText, flag = wx.RIGHT, border = 8);

        self.micCoordinateYTextControl = wx.TextCtrl (creationPanel);
        micCoordinateYBox.Add(self.micCoordinateYTextControl, proportion = 1);
        verticalBox.Add (micCoordinateYBox, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border = 10);

        verticalBox.Add((-1,5));

        buttonsBox= wx.BoxSizer (wx.HORIZONTAL);

        addButton = wx.Button(creationPanel, label = "Add");
        buttonsBox.Add (addButton, flag = wx.LEFT, border = 8);

        cancelButton = wx.Button (creationPanel, label = "Cancel");
        buttonsBox.Add (cancelButton, flag = wx.LEFT, border = 8);

        verticalBox.Add (buttonsBox, flag = wx.BOTTOM | wx.ALIGN_RIGHT, border = 10);

        creationPanel.SetSizer(verticalBox);

        self.Bind (wx.EVT_BUTTON, self.AddMic, addButton);
        self.Bind (wx.EVT_BUTTON, self.CancelAddition, cancelButton);

    def AddMic (self,event):
        print "Add Mic";
        print "Stadium Mic Quantity: " + str(stadium.MicQuantity());
        newLabel = self.labelTextControl.GetValue();
        #newWing = self.micWingTextControl.GetValue();
        newWing = self.container.GetString(self.container.GetSelection());
        newCoordinateX = int(self.micCoordinateXTextControl.GetValue());
        newCoordinateY = int(self.micCoordinateYTextControl.GetValue());

        mic = Mic(newLabel, newWing, newCoordinateX, newCoordinateY, stadium.MicQuantity());

        stadium.AddMic(mic);

        print newWing + "[" + newLabel + "]: (" + str(newCoordinateX) + "," + str(newCoordinateY) + ")";

        print "Mic Added Succesfully"
        print "Stadium Mic Quantity: " + str(stadium.MicQuantity());
        self.Close(True);



    def CancelAddition(self, event):
        self.Close(True);

class RemoveMicWindow (wx.Frame):
    def __init__(self, *args, **kwargs):
        super(RemoveMicWindow, self).__init__(*args, **kwargs);
        self.SetSize((400, 200));
        self.SetTitle("Remove Mic");
        self.Centre();
        self.Show(True);
        self.BasicGUI();

    def BasicGUI(self):

        removalPanel = wx.Panel(self);

        verticalBox = wx.BoxSizer(wx.VERTICAL);


        micUnitTextBox = wx.BoxSizer (wx.HORIZONTAL);
        micUnitStaticText = wx.StaticText (removalPanel, label = "Mic Units");
        micUnitTextBox.Add (micUnitStaticText, flag = wx.CENTER, border = 8);
        verticalBox.Add (micUnitTextBox, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border = 10);

        verticalBox.Add((-1,10));

        micOptionsBox = wx.BoxSizer (wx.HORIZONTAL);
        micOptionsStaticText = wx.StaticText (removalPanel, label = "Mic Label: ");
        micOptionsBox.Add (micOptionsStaticText, flag = wx.RIGHT, border = 8);


        micOptions = [];
        for mic in stadium.micList:
            micOptions.append(mic.label);

        self.container = wx.ListBox (removalPanel, -1, (20,20), (80,95), micOptions, wx.LB_SINGLE);
        self.container.SetSelection(0);
        micOptionsBox.Add (self.container, proportion = 1);
        verticalBox.Add (micOptionsBox, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border = 10);

        '''
        wingsList = ['East', 'North', 'South', 'West'];
        self.container = wx.ListBox (creationPanel, -1, (20,20), (80,95), wingsList, wx.LB_SINGLE);
        self.container.SetSelection(0); #default selection
        micWingBox.Add (self.container, proportion = 1);
        verticalBox.Add (micWingBox, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border = 10);
        '''
        verticalBox.Add((-1,15));

        buttonsBox= wx.BoxSizer (wx.HORIZONTAL);

        removeButton = wx.Button(removalPanel, label = "Remove");
        buttonsBox.Add (removeButton, flag = wx.LEFT, border = 8);

        cancelButton = wx.Button (removalPanel, label = "Cancel");
        buttonsBox.Add (cancelButton, flag = wx.LEFT, border = 8);

        verticalBox.Add (buttonsBox, flag = wx.BOTTOM | wx.ALIGN_RIGHT, border = 10);

        removalPanel.SetSizer(verticalBox);

        self.Bind (wx.EVT_BUTTON, self.RemoveMic, removeButton);
        self.Bind (wx.EVT_BUTTON, self.CancelAddition, cancelButton);

    def RemoveMic (self,event):
        print "Remove Mic";

        toBeRemovedLabel = self.container.GetString(self.container.GetSelection());

        for mic in stadium.micList:
            if (mic.label == toBeRemovedLabel):
                stadium.RemoveMic(mic);

        print "Mic Removed Succesfully"
        print "Stadium.MicQuantity(): " + str(stadium.MicQuantity());

        self.Close(True);



    def CancelAddition(self, event):
        self.Close(True);
        print "Operation Canceled";
        print "Stadium.MicQuantity(): " + str(stadium.MicQuantity());

def Main():
    app = wx.App();
    MainWindow(None);
    app.MainLoop();

print "Ready";

Main();
#k = input("Press close to exit");
