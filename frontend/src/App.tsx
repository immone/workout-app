import React, { useState } from 'react';
import { Button } from './components/ui/Button';
import { Input } from './components/ui/Input';  
import SimpleCalendarForm from './components/Calendar';
import { Toast } from "@/components/Toast"; 
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { sendSchedule } from '@/services/schedule';

const App: React.FC = () => {
  const [workoutName, setWorkoutName] = useState('');
  const [toastMessage, setToastMessage] = useState<string | null>(null);  
  const [chosenDays, setChosenDays] = useState<Date[]>([]);
  const [isWorkoutNameSubmitted, setIsWorkoutNameSubmitted] = useState(false);
  const [confirmedDays, setConfirmedDays] = useState<number>(-1);
  const [times, setTimes] = useState<string[]>([]);
  const [isScheduleFound, setIsScheduleFound] = useState(false);
  const [scheduleResponse, setScheduleResponse] = useState<any>(null);  // To store backend response

  const handleWorkoutNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setWorkoutName(e.target.value);
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
    setChosenDays(dates);
    setConfirmedDays(0);
  };

  const handleConfirmTimeSlot = (dayIndex: number, dayTimes: string[]) => {
    const newTimes = [...times];
    newTimes[dayIndex] = dayTimes.join(', ');
    setTimes(newTimes);
    setConfirmedDays((prev) => prev + 1);
  };

  const handleFindSchedule = async () => {
    setIsScheduleFound(true);
    console.log(times, chosenDays)
    setToastMessage("Finding your schedule...");

    try {
      const scheduleData = {
        times: times,
        days: chosenDays,
      };

      const response = await sendSchedule(scheduleData);  // API call
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
                    className="bg-blue-500 text-white rounded-corners w-full transition duration-200 hover:bg-blue-600 mb-4"
                  >
                    Submit
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
                    Select time slots for {chosenDays[confirmedDays]?.toLocaleDateString()}
                  </p>
                  <TimeSlotSelection
                    key={confirmedDays}
                    onConfirm={(dayTimes: string[]) =>
                      handleConfirmTimeSlot(confirmedDays, dayTimes)
                    }
                    setToastMessage={setToastMessage}
                  />
                </>
              ) : (
                <ConfirmedTimesView 
                  times={times} 
                  chosenDays={chosenDays} 
                  onFindSchedule={handleFindSchedule} 
                  scheduleResponse={scheduleResponse} 
                />
              )}
            </CardContent>
          </Card>
        ) : (
          <Card className="bg-zinc-900 shadow-lg rounded-corners p-8 w-[380px]">
            <CardHeader>
              <CardTitle className="text-middle text-3xl">Schedule</CardTitle>
            </CardHeader>
            <CardContent className="text-white">
              <p>Your confirmed schedule:</p>
              <ul className="list-disc">
                {times.map((timeSlot, index) => (
                  <li key={index} className="mb-2">
                    {chosenDays[index]?.toLocaleDateString()}: {timeSlot ? timeSlot : 'No time slots selected'}
                  </li>
                ))}
              </ul>
              {scheduleResponse && (
                <>
                  <p className="mt-4">Backend Response:</p>
                  <p>{scheduleResponse.message}</p>
                </>
              )}
            </CardContent>
          </Card>
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

const TimeSlotSelection: React.FC<{ onConfirm: (dayTimes: string[]) => void; setToastMessage: (message: string) => void; }> = ({
  onConfirm,
  setToastMessage,
}) => {
  const [timeSlots, setTimeSlots] = useState<string[]>([]);

  const addTimeSlot = () => {
    const newTimeSlot = '';
    if (!timeSlots.includes(newTimeSlot)) {
      setTimeSlots([...timeSlots, newTimeSlot]);
    } else {
      setToastMessage("This time slot is already added!");
    }
  };

  const removeTimeSlot = (index: number) => {
    const newTimeSlots = [...timeSlots];
    newTimeSlots.splice(index, 1);
    setTimeSlots(newTimeSlots);
  };

  const handleTimeChange = (index: number, value: string) => {
    const newTimeSlots = [...timeSlots];
    if (!newTimeSlots.includes(value) || newTimeSlots[index] === value) {
      newTimeSlots[index] = value;
      setTimeSlots(newTimeSlots);
    } else {
      setToastMessage("This time slot is already added!");
    }
  };

  return (
    <div className="flex flex-col items-center">
      {timeSlots.map((slot, index) => (
        <div key={index} className="flex space-x-2 items-center mb-2">
          <input
            type="time"
            value={slot}
            onChange={(e) => handleTimeChange(index, e.target.value)}
            className="bg-gray-800 text-white p-2 rounded"
          />
          <Button
            onClick={() => removeTimeSlot(index)}
            className="bg-red-500 text-white rounded-corners text-xs px-2 py-1"
          >
            Remove
          </Button>
        </div>
      ))}
      <Button onClick={addTimeSlot} className="bg-blue-500 text-white rounded-corners w-full mt-2">
        Add Time Slot
      </Button>
      <Button
        onClick={() => onConfirm(timeSlots.filter(slot => slot))}
        className="bg-green-500 text-white rounded-corners w-full mt-4"
      >
        Confirm Time Slots
      </Button>
    </div>
  );
};

const ConfirmedTimesView: React.FC<{ times: string[]; chosenDays: Date[]; onFindSchedule: () => void; scheduleResponse: any }> = ({
  times,
  chosenDays,
  onFindSchedule,
  scheduleResponse,
}) => {
  return (
    <div>
      <h2 className="text-lg text-white mb-4 text-center">Confirmed Times</h2>
      <ul className="text-white list-disc">
        {times.map((time, index) => (
          <li key={index}>
            {chosenDays[index]?.toLocaleDateString()}: {time ? time : "No time slots selected"}
          </li>
        ))}
      </ul>
      <Button 
        onClick={onFindSchedule}
        className="bg-green-500 text-white rounded-corners w-full mt-4"
      >
        Find Schedule
      </Button>
      {scheduleResponse && (
        <div className="mt-4">
          <p className="text-white">Backend Response:</p>
          <p className="text-white">{scheduleResponse.message}</p>
        </div>
      )}
    </div>
  );
};

export default App;
