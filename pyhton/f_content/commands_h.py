from f_content import tts_speach as tts
import nltk as n
print(n.__version__)  # Should output 3.8.1

class CommandHandler:


    def __init__(self):
        self.commands = None
        # Define the commands, actions, and targets
        self.COMMAND = ['move','rotate','stop','exit','help','status','calibrate','set','get',
            'run','pause','resume','restart','shutdown','reboot','update','upgrade','install','uninstall','list',
            'show','hide','open','close','enable','disable','start','stop','restart','reset','clear','clean',
            'save','load','create','delete','remove','add','edit','change','set','get','find','search','locate',
            'identify','scan','test','check','verify','validate','ping','pong','echo','repeat','say','speak','tell',
            'ask','answer','question','query','respond','reply','confirm','acknowledge','accept','reject','approve',
            'deny','agree','disagree','yes','no','true','false','on','off','up','down','left','right','forward',
            'backward','clockwise','counterclockwise','north','south','east','west','upward','downward','leftward',
            'rightward','forwardward','backwardward','clockwiseward','counterclockwiseward','northward','southward',
            'eastward','westward']

        self.ACTIONS = ['position','angle','speed','velocity','acceleration','distance','time','duration','rotation','direction',
                'orientation','heading','bearing','altitude','latitude','longitude','temperature','humidity','pressure',
                'light','sound','noise','vibration','force','torque','energy','power','voltage','current','resistance',
                'capacitance','inductance','frequency','phase','amplitude','waveform','signal','data','bit','byte','word',
                'integer','float','double','string','text','character','array','list','queue','stack','table','matrix',
                'graph','tree','object','class','module','function','method','variable','constant','property','attribute',
                    'parameter','argument','return','input','output','error','exception','event','message','packet','frame',
                        'block','segment','section','part','component','device','sensor','actuator','controller','driver','interface',
                        'protocol','standard','specification','format','structure','syntax','semantics','logic','algorithm',
                        'procedure','process','operation','task','job','action','activity','behavior','state','condition','mode',
                        'status','flag','bitmask','register','memory','storage','database','file','stream','channel','port',
                        'connection','link','network','system','software','firmware','hardware','firmware','interface','module',
                        'library','package','plugin','extension','tool','utility','application','program','script','code','data',
                        'information','knowledge','wisdom','intelligence','consciousness','mind','thought','idea','concept',
                        'theory','principle','law','rule','fact','evidence','proof','reason','cause','effect','result','outcome',
                        'goal','objective','target','purpose','mission','vision','strategy','plan','policy','procedure','process']

        self.TARGETS = ['motor a','servo','stepper','dc','brushless','pwm','esc','driver','controller','encoder','sensor','imu',
                    'gyro','accelerometer','magnetometer','gps','lidar','camera','lidar','radar','ultrasonic','sonar','ir',
                    'laser','temperature','humidity','pressure','light','sound','noise','vibration','force','torque',
                        'energy','power','voltage','current','resistance','capacitance','inductance','frequency','phase',
                        'amplitude','waveform','signal','data','bit','byte','word','integer','float','double','string','text',
                        'arm','grip','leds','LED','display','screen','monitor','keyboard','mouse','joystick','gamepad','remote']

        self.UNITS = ['meters', 'centimeters', 'millimeters', 'kilometers', 'inches', 'feet', 'yards', 'miles', 'radians', 'degrees',
            'revolutions', 'seconds', 'minutes', 'hours', 'days', 'weeks', 'months', 'years', 'milliseconds', 'microseconds',
                'nanoseconds', 'picoseconds', 'kiloseconds', 'megaseconds', 'gigaseconds', 'teraseconds', 'petaseconds',
                    'bytes', 'kilobytes', 'megabytes', 'gigabytes', 'terabytes', 'petabytes', 'exabytes', 'zettabytes',
                        'yottabytes', 'bits', 'kilobits', 'megabits', 'gigabits', 'terabits', 'petabits', 'exabits', 'zettabits',
                            'yottabits', 'hertz', 'kilohertz', 'megahertz', 'gigahertz', 'terahertz', 'petahertz', 'exahertz',
                                'zettahertz', 'yottahertz', 'newtons', 'pounds', 'kilograms', 'grams', 'milligrams', 'micrograms',
                                    'nanograms', 'picograms', 'kilograms', 'megagrams', 'gigagrams', 'teragrams', 'petagrams',
                                        'exagrams', 'zettagrams', 'yottagrams', 'watts', 'kilowatts', 'megawatts', 'gigawatts',
                                            'terawatts', 'petawatts', 'exawatts', 'zettawatts', 'yottawatts', 'volts', 'millivolts',
                                                'microvolts', 'nanovolts', 'picovolts', 'kilovolts', 'megavolts', 'gigavolts',
                                                    'teravolts', 'petavolts', 'exavolts', 'zettavolts', 'yottavolts', 'amperes',
                                                        'milliamperes', 'microamperes', 'nanoamperes', 'picoamperes', 'kiloamperes',
                                                            'megaamperes', 'gigaamperes', 'teraamperes', 'petaamperes', 'exaamperes',
                                                                'zettaamperes', 'yottaamperes', 'ohms', 'milliohms', 'microohms', 'º', '°']

        self.DIRECTION = ['up','down','left','right','forward','backward','clockwise','counterclockwise','north','south','east','west']

        n.download('punkt')
        n.download('averaged_perceptron_tagger')


    def parse_command(self,sentence):
        # Tokenize and tag the words
        tokens = n.word_tokenize(sentence.lower())
        tagged_tokens = n.pos_tag(tokens)
        
        # Initialize command structure
        command = {
            "command": None,
            "action": None,
            "target": None,
            "parameters": {},
            "units": None,
            "direction": None
        }
        

        # Step 1: Identify target (e.g., "motor 1") If there is no target, we assume its a chat command
        for target in self.TARGETS:
            if target in sentence.lower():
                command["target"] = target.replace(" ", "_").upper()
                break
        
        if command["target"] is not None:
            # Step 1: Find command intent
            for word, tag in tagged_tokens:
                if word in self.COMMAND:
                    command["command"] = word.upper()
                    break

            # Step 3: Identify action and parameters
            for i, (word, tag) in enumerate(tagged_tokens):
                # Check for action keywords
                if word in self.ACTIONS or (word in self.COMMAND and word != command["command"]):
                    command["action"] = word.upper()
                    
                    # Find if there is a unit in the tagged tokens
                    if 'CD' in [tag for word, tag in tagged_tokens]:
                        for unit in self.UNITS:
                            if unit in sentence.lower():
                                command["units"] = unit
                                break
                        for j, (word, tag) in enumerate(tagged_tokens):
                            if tag == 'CD':
                                command["parameters"][word] = tagged_tokens[j][0]

            # Step 4: If there is a direction detect it
            for direction in self.DIRECTION:
                if direction in sentence.lower():
                    command["direction"] = direction.upper()
                    break

            return command
        
        else:
            if "reboot" in sentence.lower() or "restart" in sentence.lower():
                return "reboot"
            elif "shut down" in sentence.lower():
                return "shutdown"
            else:
                return "sentence is not a command"

# Example Usage

''''n.download()
n.download('punkt')
n.download('averaged_perceptron_tagger')

command_handler = CommandHandler()
parsed_command = command_handler.parse_command("Move motor to position 90 degrees forward.")
print(parsed_command)'''