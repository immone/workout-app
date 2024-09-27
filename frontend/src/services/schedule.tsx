import axios from 'axios';

export interface Schedule {
    times: string[];
    days: Date[];
}

export const sendSchedule = async (params: Schedule) => {
    console.log(params.times, params.days)
    try {
        const response = await axios.post('http://localhost:5000/api/schedule', params);
        console.log('Schedule sent successfully:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error sending schedule:', error);
        throw error;
    }
};
