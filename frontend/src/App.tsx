import React, { useState } from 'react';
import { Button } from './components/ui/Button';
import { Input } from './components/ui/Input';  
import SimpleCalendarForm from './components/Calendar';
import { Toast } from "@/components/Toast"; 
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { sendSchedule } from '@/services/schedule';


const App: React.FC = () => {
  const [workoutName, setWorkoutName] = useState('');
  const [preferredWorkouts, setPreferredWorkouts] = useState<number | ''>(''); 
  const [currentWorkoutInput, setCurrentWorkoutInput] = useState<number | ''>(''); 
  const [toastMessage, setToastMessage] = useState<string | null>(null);  
  const [chosenDays, setChosenDays] = useState<Date[]>([]);
  const [isWorkoutNameSubmitted, setIsWorkoutNameSubmitted] = useState(false);
  const [confirmedDays, setConfirmedDays] = useState<number>(-1);
  const [times, setTimes] = useState<string[][]>([]); 
  const [isScheduleFound, setIsScheduleFound] = useState(false);
  const [scheduleResponse, setScheduleResponse] = useState<any>(null);

  const handleWorkoutNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setWorkoutName(e.target.value);
  };

  const handleCurrentWorkoutInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;

    if (value === '' || /^[1-9]\d*$/.test(value)) {
      setCurrentWorkoutInput(value === '' ? '' : Number(value));
    }
  };

  const handlePreferredWorkoutsConfirm = () => {
    if (currentWorkoutInput === '') {
      setToastMessage('Please enter a preferred number of workouts!');
    } else {
      setPreferredWorkouts(currentWorkoutInput);
      setToastMessage(`Preferred number of workouts set to: ${currentWorkoutInput}`);
      setCurrentWorkoutInput('');
    }
  };

  const handleSubmit = () => {
    if (!workoutName.trim()) {
      setToastMessage('Please enter a workout name before submitting!');
    } else {
      setIsWorkoutNameSubmitted(true);
      setToastMessage(`Workout name set to: ${workoutName}`);
    }
  };

  const handleDateSelection = (dates: Date[]) => {
    // Sort the selected dates in chronological order
    const sortedDates = dates.sort((a, b) => a.getTime() - b.getTime());
    setChosenDays(sortedDates);
    setConfirmedDays(0);
    setTimes(Array(sortedDates.length).fill([])); 
  };
  const handleConfirmTimeSlot = (dayIndex: number, dayTimes: string[]) => {
    const newTimes = [...times];
    newTimes[dayIndex] = dayTimes; 
    setTimes(newTimes);
    setConfirmedDays((prev) => prev + 1);
  };

  const handleFindSchedule = async () => {
    setIsScheduleFound(true);
    setToastMessage("Finding your schedule...");

    try {
      const scheduleData = {
        times: times,
        days: chosenDays,
        n: Math.min(times.length, preferredWorkouts)
      };

      const response = await sendSchedule(scheduleData);  
      setToastMessage("Schedule sent successfully!");
      setScheduleResponse(response);  
    } catch (error) {
      setToastMessage("Failed to send schedule.");
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-zinc-950 font-sans">
      {toastMessage && <Toast message={toastMessage} />}
      
      <header className="py-4 text-center relative z-10">
        <h1 className="scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight first:mt-0">
          Workout Scheduler
        </h1>
        <p className="mt-2 text-lg text-white opacity-80 text-border">
          Plan your workouts effectively
        </p>
      </header>
      
      <main className="flex-grow flex flex-col items-center space-y-4">
        {!isScheduleFound ? (
          <Card className="bg-zinc-900 shadow-lg rounded-corners p-8 w-[380px]">
            <CardHeader>
              <CardTitle className="text-middle text-3xl">Scheduler</CardTitle>
              <CardDescription>Choose suitable days and time slots</CardDescription>
            </CardHeader>
            <CardContent className="flex flex-col items-center">
              {!isWorkoutNameSubmitted ? (
                <>
                  <Input 
                    type="text" 
                    placeholder="Enter your workout name" 
                    value={workoutName}
                    onChange={handleWorkoutNameChange} 
                    className="mb-4 border border-blue-300 rounded focus:outline-none focus:ring focus:ring-blue-400 bg-gray-800 text-white text-center"
                  />
                  <Button 
                    onClick={handleSubmit}
                    className="bg-green-500 text-white rounded-corners w-full transition duration-200 hover:bg-blue-600 mb-4"
                  >
                    Submit
                  </Button>
                </>
              ) : preferredWorkouts === '' ? (
                <>
                  <Input
                    type="text"
                    placeholder="Preferred number of workouts"
                    value={currentWorkoutInput} 
                    onChange={handleCurrentWorkoutInputChange} 
                    className="mb-4 border border-blue-300 rounded focus:outline-none focus:ring focus:ring-blue-400 bg-gray-800 text-white text-center"
                  />
                  <Button 
                    onClick={handlePreferredWorkoutsConfirm}
                    className="bg-green-500 text-white rounded-corners transition duration-200 hover:bg-blue-600 mb-4"
                  >
                    Confirm
                  </Button>
                </>
              ) : chosenDays.length === 0 ? (
                <div>
                  <SimpleCalendarForm 
                    onDateSelection={handleDateSelection}
                    onToastMessage={setToastMessage} 
                  />
                </div>
              ) : confirmedDays < chosenDays.length ? (
                <>
                  <p className="text-white mb-4">
                    Select clock times for {chosenDays[confirmedDays]?.toLocaleDateString()}
                  </p>
                  <ClockTimeSlotSelection
                    key={confirmedDays}
                    onConfirm={(dayTimes: string[]) =>
                      handleConfirmTimeSlot(confirmedDays, dayTimes)
                    }
                    setToastMessage={setToastMessage}
                  />
                </>
              ) : (
                <ConfirmedTimesView 
                  onFindSchedule={handleFindSchedule} 
                  scheduleResponse={scheduleResponse} 
                />
              )}
            </CardContent>
          </Card>
        ) : (
          <ScheduleDisplay scheduleResponse={scheduleResponse} />
        )}
      </main>

      <footer className="py-4 text-center">
        <p className="text-gray-400">
          © 2024 Workout Scheduler. All rights reserved.
        </p>
      </footer>
    </div>
  );
};

const ClockTimeSlotSelection: React.FC<{ onConfirm: (dayTimes: string[]) => void; setToastMessage: (message: string) => void; }> = ({
  onConfirm,
  setToastMessage,
}) => {
  const availableTimes = [
    '08:00', '09:00', '10:00', '11:00',
    '12:00', '13:00', '14:00', '15:00',
    '16:00', '17:00', '18:00', '19:00',
    '20:00', '21:00'
  ];

  const [selectedTimes, setSelectedTimes] = useState<string[]>([]);

  const handleTimeToggle = (time: string) => {
    setSelectedTimes((prev) => 
      prev.includes(time) 
        ? prev.filter(t => t !== time) 
        : [...prev, time] 
    );
  };

  const handleConfirm = () => {
    if (selectedTimes.length === 0) {
      setToastMessage("Please select at least one time slot!");
      return;
    }
    onConfirm(selectedTimes);
  };

  return (
    <div className="flex flex-col items-center">
      <p className="text-white mb-4">Select your preferred times:</p> {/* Added mb-4 for margin-bottom */}
      <div className="grid grid-cols-2 gap-2">
        {availableTimes.map((time) => (
          <Button
            key={time}
            className={`transition duration-200 ${selectedTimes.includes(time) ? 'bg-green-500' : 'bg-blue-500'} text-white rounded-corners w-full`}
            onClick={() => handleTimeToggle(time)}
          >
            {time}
          </Button>
        ))}
      </div>
      <Button
        className="mt-4 bg-green-500 text-white rounded-corners"
        onClick={handleConfirm}
      >
        Confirm time
      </Button>
    </div>
  );
};

const ConfirmedTimesView: React.FC<{ onFindSchedule: () => void; scheduleResponse: any; }> = ({ onFindSchedule }) => {
  return (
    <div className="flex flex-col items-center mt-4">
      <p className="text-white">Times confirmed!</p>
      <Button className="mt-4 bg-green-500 text-white rounded-corners" onClick={onFindSchedule}>
        Find My Schedule
      </Button>
    </div>
  );
};

const ScheduleDisplay: React.FC<{ scheduleResponse: any; }> = ({ scheduleResponse }) => {
  return (
    <Card className="bg-zinc-900 shadow-lg rounded-corners p-8 w-[380px]">
      <CardHeader>
        <CardTitle className="text-middle text-3xl">Your Schedule</CardTitle>
      </CardHeader>
      <CardContent>
        {Array.isArray(scheduleResponse?.solution) && scheduleResponse.solution.length > 0 ? (
          <ul className="text-white">
            {scheduleResponse.solution.map((item: [string, string], index: number) => (
              <li key={index}>
                {item[0]}: {item[1]}
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-white">No available schedule found.</p>
        )}
      </CardContent>
    </Card>
  );
};

export default App;
