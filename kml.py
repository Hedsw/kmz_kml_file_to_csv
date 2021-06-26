from bs4 import BeautifulSoup
import csv
import os
class get_columns:
    def process_coordinate_string(list_test):
        """
        Take the coordinate string from the KML file, and break it up into [SiteName, Latitude, Longitude, Type] for a CSV row and other columns
        """
        ret = []
        ret.append(list_test[0])              # Site Name 
        ret.append(list_test[1])              # Water Types 
        ret.append(list_test[2])              # Longitude  
        print(list_test[2], list_test[3]) # Lat, long

        coordstr = list_test[2].rstrip('\n')  # Latitude  
        space_splits = coordstr.split(" ")
        #take out the empty values
        space_splits = list(filter(None, space_splits))
    #    # There was a space in between <coordinates>" "-80.123...... hence the [1:]
        # For 2019_06_25_26.kml, we have to remove below for loop
        for split in space_splits[1:]:
            comma_split = split.split(',')
            ret.append(comma_split[1])    # lat
            ret.append(comma_split[0])    # lng
            #to test the output: print(ret)
        ret.append(list_test[3])   #Long, Latitude Split
        return ret

class kml_to_csv_class:
    water = [
    'F3D1S4', 'F3D1S6', 'F3D1S7', 'F3D1S8',
    'F3D1S9', 'F3D1S11', 'F3D1S12', 'F3D1S13',
    'F3D1S14', 'F3D1S14', 'F3D1S15', 'F3D1S16',
    'F3D1S17', 'F3D1S17', 'F3D1S18', 'F3D1S19',
    'F3D1S120', 'F3D1S20', 'F3D2S1', 'F3D2S2',
    'F3D2S4', 'F3D2S13', 'F3D2S14', 'F3D2S15',
    'F3D2S16', 'F3D2S18', 'F3D2S19', 'F3D2S20',
    'F3D3S1', 'F3D3S1', 'F3D3S2', 'F3D3S2',
    'F3D3S3', 'F3D3S5', 'F3D3S77', 'F3D3S9',
    'F3D3S10', 'F3D3S12', 'F3D3S13', 'F3D3S15',
    'F3D3S16', 'F3D3S16', 'F3D3S17', 'F3D3S18',
    'F3D3S18', 'F3D3S19', 'F3D3S20', 'F3D3S21',
    'F3D3S22', 'F3D3S25', 'F3D3S25', 'F3D3S26',
    'F3D3S27', 'F3D3S27', 'F3D3S28', 'F3D3S28',
    'F3D3S29', 'F3D4S2', 'F3D4S2', 'F3D4S3',
    'F3D4S4', 'F3D4S4', 'F3D4S5', 'F3D4S6',
    'F3D4S77', 'F3D4S77', 'F3D4S9', 'F3D4S10',
    'F3D5S3', 'F3D5S4', 'F3D5S6', 'F3D5S7',
    'mix19', 'mix19', 'mixa1', 'mixa3',
    'NW15', 'NW16', 'NW16', 'w11',
    'w16', 'w17', 'w20', 'w20'
] 

    non_water = [
    'F3D2S6', 'F3D2S12', 'F3D2S17', 'F3D3S6', 
    'F3D3S8', 'F3D5S9', 'F3D5S2', 'F3D5S10', 
    'F3D5S11', 'F3D5S12', 'mix1', 'mix2', 
    'mix3', 'mix5', 'mix6', 'mix7', 
    'mix8', 'mix9', 'mix11', 'mix12', 
    'mix13', 'mix13', 'mix16', 'mix18', 
    'mix20', 'mixa2', 'mixa4', 'mixa5', 'mixa7', 
    'mixa8', 'mixa9', 'mixa10', 'mixa11', 
    'mixa12', 'mixa12', 'mixa12', 'mixa13',
    'mixa15', 'mixa16', 'mixa17', 'mixa17',
    'mixa18', 'mixa19', 'mixa20', 'nw1',
    'NW6', 'NW7', 'NW7', ' NW11',
    'NW13', 'NW13', 'NW14', 'NW17',
    'nwa2', 'nwa3', 'nwa4', 'nwa5',
    'nwa7', 'nwa8', 'nwa9', 'nwa10',
    'nwa11', 'nwa12', 'nwa13', 'nwa14',
    'nwa14', 'nwa15', 'nwa16', 'nwa16',
    'nwa16', 'nwa17', 'nwa18', 'nwa19',
    'nwa20', 'w4', 'w6', 'w7',
    'w18', 'w19'
]

    def kml_to_csv(rootDir, kmlFile, csvFile, company_name):
        """
        Open the KML. Read the KML. Open a CSV file. Process a coordinate string to be a CSV row.
        """
        with open(rootDir + kmlFile, encoding='utf8') as f:
            s = BeautifulSoup(f, 'xml')
            with open(rootDir + csvFile, 'w', newline='', encoding='utf8') as csvfile:
                #Define the headers
                header = ['Site name','Water Type', 'Longitude' ,'Latitude']
                writer = csv.writer(csvfile)
                writer.writerow(header)
                total_list = []
                print(s)
                for placemark in s.find_all('Placemark'):
                    #print(placemark)
                    #added conditions for no values in child tags
                    name = placemark.find('name').string  \
                        if placemark.find('name') is not None  \
                        else 'None'
                    description = placemark.find('description').string  \
                                if placemark.find('description') is not None  \
                                else 'None'
                    coords = placemark.find('coordinates').string \
                            if placemark.find('coordinates') is not None  \
                            else 'None'
                    
                    types = "not used"
                    namelower = name.lower()
                    nameupper = name.upper()
                    #print(namelower)
                    #print(nameupper)
                    if namelower in kml_to_csv_class.water or nameupper in kml_to_csv_class.water:
                        types = "water"
                    elif namelower in kml_to_csv_class.non_water or nameupper in kml_to_csv_class.non_water:
                        types = "nonwater"
                    else:
                        types = "not used"
                    
                    
                    #create a list for and append values for each row
                    list_test = []
                    parse_coords = coords.split(',')
                    #print(parse_coords[0] , parse_coords[1])
                    list_test.extend((name, types, parse_coords[0], parse_coords[1]))
                    total_list.append(get_columns.process_coordinate_string(list_test))
                    #print(coords.string)
                    #print(total_list)
                writer.writerows(total_list)

def main():  
    #Define the absolute path
    abs_path = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    filename = input("Please insert [[KML]] File name with file type! ex) i3.kml  :")
    
    csvName = filename
    csvName = csvName.replace('.kml','.csv')
    print(csvName)
    
    kml_to_csv_class.kml_to_csv('', filename, csvName, '')

if __name__ == "__main__":
    main()
    